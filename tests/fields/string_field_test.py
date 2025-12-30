import unittest
from bluetti_bt_lib.fields import StringField, FieldName


class TestStringField(unittest.TestCase):
    def setUp(self):
        self.field = StringField(FieldName.DEVICE_TYPE, 10, 6)

    def test_parse(self):
        result = self.field.parse(b"\x45\x42\x33\x41\x00\x00")
        self.assertEqual(result, "EB3A")

        result = self.field.parse(b"\x41\x43\x33\x30\x30\x00")
        self.assertEqual(result, "AC300")

    def test_is_writeable(self):
        self.assertFalse(self.field.is_writeable())
