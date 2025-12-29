import unittest

from bluetti_bt_lib.registers import ReadableRegisters


class TestReadableRegisters(unittest.TestCase):
    def setUp(self):
        self.register = ReadableRegisters(100, 2)

    def test_initialization(self):
        self.assertEqual(self.register.register_action.value, 3)
        self.assertEqual(self.register.cmd[1], 3)

    def test_response_size(self):
        self.assertEqual(self.register.response_size(), 9)

    def test_parse_response(self):
        response = b"\x01\x03\x04\x00\x64\x00\x00\x79\x84"
        parsed = self.register.parse_response(response)
        self.assertEqual(parsed, b"\x00\x64\x00\x00")

    def test_parse_response_invalid_size(self):
        response = b"\x01\x03\x04\x00\x64"
        with self.assertRaises(ValueError):
            self.register.parse_response(response)
