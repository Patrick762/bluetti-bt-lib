import unittest
from bluetti_bt_lib.fields import SwitchField, FieldName


class TestSwitchField(unittest.TestCase):
    def setUp(self):
        self.field = SwitchField(FieldName.CTRL_AC, 100)

    def test_parse_true(self):
        result = self.field.parse(b"\x00\x01")
        self.assertTrue(result)

    def test_parse_false(self):
        result = self.field.parse(b"\x00\x00")
        self.assertFalse(result)

    def test_parse_invalid(self):
        result = self.field.parse(b"\x00\x05")
        self.assertIsNone(result)

    def test_is_writeable(self):
        self.assertTrue(self.field.is_writeable())

    def test_allowed_write_type(self):
        self.assertTrue(self.field.allowed_write_type(True))
        self.assertTrue(self.field.allowed_write_type(False))
        self.assertFalse(self.field.allowed_write_type(1))
        self.assertFalse(self.field.allowed_write_type("true"))
