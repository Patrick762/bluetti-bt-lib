from decimal import Decimal
import unittest
from bluetti_bt_lib.fields import VersionField, FieldName


class TestVersionField(unittest.TestCase):
    def setUp(self):
        self.field = VersionField(FieldName.VER_ARM, 23)

    def test_parse(self):
        result = self.field.parse(b"\x91\x96\x00\x01")
        self.assertEqual(result, Decimal("1028.06"))

    def test_parse_invalid_length(self):
        result = self.field.parse(b"\x00\x01")
        self.assertIsNone(result)

    def test_is_writeable(self):
        self.assertFalse(self.field.is_writeable())
