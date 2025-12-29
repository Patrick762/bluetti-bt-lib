import unittest

from bluetti_bt_lib.registers import WriteableRegister


class TestWriteableRegister(unittest.TestCase):
    def setUp(self):
        self.register = WriteableRegister(100, 1)

    def test_initialization(self):
        self.assertEqual(self.register.register_action.value, 6)
        self.assertEqual(self.register.cmd[1], 6)

    def test_parse_response(self):
        response = b"\x01\x03\x04\x00\x01\x00\x00\x79"
        parsed = self.register.parse_response(response)
        self.assertEqual(parsed, b"\x01\x00")
