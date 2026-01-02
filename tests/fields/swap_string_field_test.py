import unittest
from bluetti_bt_lib.fields import SwapStringField, FieldName


class TestSwapStringField(unittest.TestCase):
    def setUp(self):
        self.field = SwapStringField(FieldName.DEVICE_TYPE, 110, 6)

    def test_parse(self):
        result = self.field.parse(b"\x50\x45\x30\x36\x00\x30")
        self.assertEqual(result, "EP600")

        result = self.field.parse(b"\x50\x45\x30\x32\x30\x30")
        self.assertEqual(result, "EP2000")

    def test_is_writeable(self):
        self.assertFalse(self.field.is_writeable())
