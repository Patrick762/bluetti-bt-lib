"""Tests for the Bluetti test device mock framework."""

import struct
import unittest

from bleak import BleakError

from bluetti_bt_lib.registers import ReadableRegisters, WriteableRegister

from tests.bluetti_test_device import (
    RegisterMemory,
    MODBUSHandler,
    FailureInjector,
    ConnectionErrorType,
)


class TestRegisterMemory(unittest.TestCase):
    def test_write_and_read_single_register(self):
        memory = RegisterMemory()
        memory.write_register(50, b"\x01\x23")
        data = memory.read_registers(50, 1)
        self.assertEqual(data, b"\x01\x23")

    def test_read_uninitialized_register_returns_zeros(self):
        memory = RegisterMemory()
        data = memory.read_registers(50, 1)
        self.assertEqual(data, b"\x00\x00")

    def test_write_and_read_multiple_registers(self):
        memory = RegisterMemory()
        memory.write_registers(10, b"\x00\x01\x00\x02\x00\x03")
        data = memory.read_registers(10, 3)
        self.assertEqual(data, b"\x00\x01\x00\x02\x00\x03")


class TestMODBUSHandler(unittest.TestCase):
    def setUp(self):
        self.memory = RegisterMemory()
        self.memory.write_register(10, struct.pack("!H", 100))
        self.memory.write_register(11, struct.pack("!H", 200))
        self.memory.write_register(12, struct.pack("!H", 300))
        self.handler = MODBUSHandler(self.memory, [range(0, 100)], [range(50, 60)])

    def test_read_holding_registers_success(self):
        cmd = ReadableRegisters(10, 3)
        response = self.handler.handle_command(bytes(cmd))
        self.assertEqual(response, b"\x01\x03\x06\x00d\x00\xc8\x01,\xd1\x0e")

    def test_read_holding_registers_not_readable(self):
        cmd = ReadableRegisters(99, 5)
        response = self.handler.handle_command(bytes(cmd))
        self.assertEqual(response, b"\x01\x83\x02\xc0\xf1")

    def test_write_single_register_success(self):
        cmd = WriteableRegister(55, 500)
        response = self.handler.handle_command(bytes(cmd))

        # Response should echo back the command
        self.assertEqual(response, bytes(cmd))

        # Verify register was written
        data = self.memory.read_registers(55, 1)
        self.assertEqual(struct.unpack("!H", data)[0], 500)

    def test_write_single_register_not_writable(self):
        cmd = WriteableRegister(10, 999)  # Address 10 is not writable
        response = self.handler.handle_command(bytes(cmd))

        # Should be MODBUS exception response
        self.assertEqual(response[1], 0x86)  # function code 6 + 0x80
        self.assertEqual(response[2], MODBUSHandler.ILLEGAL_DATA_ADDRESS)

    def test_write_multiple_registers_success(self):
        # WriteMultipleRegisters(50, struct.pack("!3H", 111, 222, 333))
        cmd_bytes = b"\x01\x10\x002\x00\x03\x06\x00o\x00\xde\x01M2#"
        response = self.handler.handle_command(cmd_bytes)

        # Verify response
        self.assertEqual(response, b"\x01\x10\x00\x32\x00\x03!\xc7")

        # Verify registers were written
        data = self.memory.read_registers(50, 3)
        self.assertEqual(struct.unpack("!3H", data), (111, 222, 333))

    def test_write_multiple_registers_not_writable(self):
        # WriteMultipleRegisters(59, struct.pack("!3H", 111, 222, 333))
        cmd_bytes = b"\x01\x10\x00;\x00\x03\x06\x00o\x00\xde\x01M\xe2\x0c"
        response = self.handler.handle_command(cmd_bytes)

        # Should be MODBUS exception response
        self.assertEqual(response[1], 0x90)  # function code 0x10 + 0x80
        self.assertEqual(response[2], MODBUSHandler.ILLEGAL_DATA_ADDRESS)

    def test_invalid_crc_raises_error(self):
        cmd_bytes = bytearray([1, 3, 0, 10, 0, 1, 0xFF, 0xFF])  # Bad CRC
        with self.assertRaises(ValueError):
            self.handler.handle_command(bytes(cmd_bytes))


class TestFailureInjector(unittest.TestCase):
    def setUp(self):
        self.injector = FailureInjector()

    def test_inject_and_consume_timeout(self):
        self.assertFalse(self.injector.should_timeout())

        self.injector.inject_timeout(2)
        self.assertTrue(self.injector.should_timeout())
        self.assertTrue(self.injector.should_timeout())
        self.assertFalse(self.injector.should_timeout())

    def test_inject_and_consume_crc_error(self):
        self.assertFalse(self.injector.should_corrupt_crc())

        self.injector.inject_crc_error(1)
        self.assertTrue(self.injector.should_corrupt_crc())
        self.assertFalse(self.injector.should_corrupt_crc())

    def test_inject_and_consume_connection_error(self):
        self.assertIsNone(self.injector.should_fail_connection())

        self.injector.inject_connection_error(ConnectionErrorType.BLEAK, 1)
        exc = self.injector.should_fail_connection()
        self.assertIsInstance(exc, BleakError)
        self.assertIsNone(self.injector.should_fail_connection())

    def test_response_override(self):
        self.assertIsNone(self.injector.get_response_override())

        test_response = b"\x01\x03\x04\x00\x00\x00\x00\x00\x00"
        self.injector.override_next_response(test_response)
        self.assertEqual(self.injector.get_response_override(), test_response)
        self.assertIsNone(self.injector.get_response_override())

    def test_ordering(self):
        self.injector.inject_timeout()
        self.injector.inject_crc_error()
        self.assertIsNone(self.injector.get_response_override())
        self.assertIsNone(self.injector.should_fail_connection())
        self.assertFalse(self.injector.should_corrupt_crc())
        self.assertTrue(self.injector.should_timeout())
        self.assertTrue(self.injector.should_corrupt_crc())


if __name__ == "__main__":
    unittest.main()
