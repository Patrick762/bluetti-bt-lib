from decimal import Decimal
import unittest
from bluetti_bt_lib.fields import DecimalField, FieldName


class TestDecimalField(unittest.TestCase):
    def test_parse_scale_0(self):
        self.field = DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 0)
        result = self.field.parse(b"\x00\x10")
        self.assertEqual(result, 16)

    def test_parse_scale_1(self):
        self.field = DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314)
        result = self.field.parse(b"\x00\x11")
        self.assertEqual(result, Decimal("1.7"))

    def test_parse_scale_2(self):
        self.field = DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 2)
        result = self.field.parse(b"\x00\x13")
        self.assertEqual(result, Decimal("0.19"))

    def test_parse_scale_3(self):
        self.field = DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 3)
        result = self.field.parse(b"\x00\x23")
        self.assertEqual(result, Decimal("0.035"))

    def test_is_writeable(self):
        self.field = DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314)
        self.assertFalse(self.field.is_writeable())
