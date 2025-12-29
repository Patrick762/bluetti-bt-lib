import unittest

import crcmod
from bluetti_bt_lib.registers import DeviceRegister, RegisterAction

modbus_crc = crcmod.predefined.mkCrcFun("modbus")


class TestDeviceRegister(unittest.TestCase):
    def setUp(self):
        self.register = DeviceRegister(RegisterAction.READ, b"\x00\x01")

    def test_command_construction(self):
        expected_cmd = bytearray(b"\x01\x03\x00\x01")
        self.assertEqual(self.register.cmd[:-2], expected_cmd)

        expected_crc = modbus_crc(expected_cmd)
        actual_crc = int.from_bytes(self.register.cmd[-2:], byteorder="little")
        self.assertEqual(expected_crc, actual_crc)

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.register.response_size()

        with self.assertRaises(NotImplementedError):
            self.register.parse_response(b"\x01\x03")
