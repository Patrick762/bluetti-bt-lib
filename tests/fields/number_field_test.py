import struct
import unittest

from bluetti_bt_lib.fields import NumberField, FieldName


class TestNumberField(unittest.TestCase):
    def test_is_writeable(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertTrue(field.is_writeable())

    def test_allowed_write_type_int(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertTrue(field.allowed_write_type(50))

    def test_allowed_write_type_float(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertTrue(field.allowed_write_type(50.5))

    def test_allowed_write_type_string(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertFalse(field.allowed_write_type("50"))

    def test_allowed_write_type_bool(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        # bool is a subclass of int in Python, so this is expected to be True
        self.assertTrue(field.allowed_write_type(True))

    def test_parse(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        data = struct.pack("!H", 75)
        self.assertEqual(field.parse(data), 75)

    def test_in_range_valid(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertTrue(field.in_range(50))
        self.assertTrue(field.in_range(0))
        self.assertTrue(field.in_range(100))

    def test_in_range_below_min(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertFalse(field.in_range(-1))

    def test_in_range_above_max(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertFalse(field.in_range(101))

    def test_address(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertEqual(field.address, 2022)

    def test_size(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertEqual(field.size, 1)

    def test_name(self):
        field = NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100)
        self.assertEqual(field.name, FieldName.BATTERY_SOC_RANGE_START.value)
