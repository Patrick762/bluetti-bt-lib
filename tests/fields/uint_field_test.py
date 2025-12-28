import unittest
from bluetti_bt_lib.fields import UIntField, FieldName


class TestUIntField(unittest.TestCase):
    def test_parse(self):
        self.field = UIntField(FieldName.BATTERY_SOC, 43)
        result = self.field.parse(b"\x00\x63")
        self.assertEqual(result, 99)

    def test_parse_over_max(self):
        self.field = UIntField(FieldName.BATTERY_SOC, 43, max=100)
        result = self.field.parse(b"\x00\x65")
        self.assertEqual(result, 101)
        self.assertFalse(self.field.in_range(result))

    def test_parse_below_min(self):
        self.field = UIntField(FieldName.BATTERY_SOC, 43, min=10)
        result = self.field.parse(b"\x00\x02")
        self.assertEqual(result, 2)
        self.assertFalse(self.field.in_range(result))

    def test_is_writeable(self):
        self.field = UIntField(FieldName.BATTERY_SOC, 43)
        self.assertFalse(self.field.is_writeable())
