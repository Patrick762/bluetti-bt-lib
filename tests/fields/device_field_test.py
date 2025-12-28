import unittest
from bluetti_bt_lib.fields import DeviceField, FieldName


class TestDeviceField(unittest.TestCase):
    def test_constructor(self):
        field = DeviceField(FieldName.CTRL_AC, 100, 2)
        self.assertEqual(field.name, FieldName.CTRL_AC.value)
        self.assertEqual(field.address, 100)
        self.assertEqual(field.size, 2)

    def test_parse_not_implemented(self):
        field = DeviceField(FieldName.CTRL_AC, 100, 2)
        with self.assertRaises(NotImplementedError):
            field.parse(b"\x00\x01")

    def test_is_writeable_default(self):
        field = DeviceField(FieldName.CTRL_AC, 100, 2)
        self.assertFalse(field.is_writeable())

    def test_allowed_write_type_default(self):
        field = DeviceField(FieldName.CTRL_AC, 100, 2)
        self.assertFalse(field.allowed_write_type(123))
        self.assertFalse(field.allowed_write_type(True))
        self.assertFalse(field.allowed_write_type("test"))

    def test_in_range_default(self):
        field = DeviceField(FieldName.CTRL_AC, 100, 2)
        self.assertTrue(field.in_range(123))
        self.assertTrue(field.in_range(-1))
        self.assertTrue(field.in_range(0))
