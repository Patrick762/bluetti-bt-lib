import unittest
from bluetti_bt_lib.fields import IntField, FieldName


class TestIntField(unittest.TestCase):
    def test_parse(self):
        self.field = IntField(FieldName.AC_INPUT_POWER, 146)
        result = self.field.parse(b"\x00\x63")
        self.assertEqual(result, 99)

    def test_parse_negative(self):
        self.field = IntField(FieldName.AC_INPUT_POWER, 146)
        result = self.field.parse(b"\xff\xc0")
        self.assertEqual(result, -64)
        self.assertTrue(self.field.in_range(result))

    def test_parse_multiplier(self):
        self.field = IntField(FieldName.AC_INPUT_POWER, 146, -1)
        result = self.field.parse(b"\xff\xc0")
        self.assertEqual(result, 64)

    def test_parse_zero_negative_multiplier(self):
        self.field = IntField(FieldName.AC_INPUT_CURRENT, 1315, -0.1)
        result = self.field.parse(b"\x00\x00")
        self.assertEqual(str(result), "0.0")

    def test_parse_over_max(self):
        self.field = IntField(FieldName.AC_INPUT_POWER, 146, max=100)
        result = self.field.parse(b"\x00\x65")
        self.assertEqual(result, 101)
        self.assertFalse(self.field.in_range(result))

    def test_parse_below_min(self):
        self.field = IntField(FieldName.AC_INPUT_POWER, 146, min=-10)
        result = self.field.parse(b"\xff\xc0")
        self.assertEqual(result, -64)
        self.assertFalse(self.field.in_range(result))

    def test_is_writeable(self):
        self.field = IntField(FieldName.AC_INPUT_POWER, 146)
        self.assertFalse(self.field.is_writeable())
