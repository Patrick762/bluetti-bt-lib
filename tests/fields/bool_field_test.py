import unittest
from bluetti_bt_lib.fields import BoolField, FieldName


class TestBoolField(unittest.TestCase):
    def setUp(self):
        self.field = BoolField(FieldName.CTRL_AC, 100)

    def test_parse_true(self):
        result = self.field.parse(b"\x00\x01")
        self.assertTrue(result)

    def test_parse_false(self):
        result = self.field.parse(b"\x00\x00")
        self.assertFalse(result)

    def test_parse_invalid(self):
        result = self.field.parse(b"\x00\x05")
        self.assertIsNone(result)
