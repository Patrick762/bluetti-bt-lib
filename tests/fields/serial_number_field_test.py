import unittest
from bluetti_bt_lib.fields import SerialNumberField, FieldName


class TestSerialNumberField(unittest.TestCase):
    def setUp(self):
        self.field = SerialNumberField(FieldName.DEVICE_SN, 116)

    def test_parse(self):
        result = self.field.parse(b"\x00\x01\x00\x00\x00\x00\x00\x00")
        self.assertEqual(result, 1)

    def test_parse_invalid_length(self):
        result = self.field.parse(b"\x00\x01\x00\x01")
        self.assertIsNone(result)

    def test_is_writeable(self):
        self.assertFalse(self.field.is_writeable())
