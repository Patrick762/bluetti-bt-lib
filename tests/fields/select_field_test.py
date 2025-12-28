from enum import Enum
import unittest
from bluetti_bt_lib.fields import SelectField, FieldName


class Dummy(Enum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2


class Dummy2(Enum):
    VALUE_6 = 6
    VALUE_3 = 3
    VALUE_8 = 8


class TestSelectField(unittest.TestCase):
    def test_parse(self):
        field = SelectField(FieldName.AC_OUTPUT_MODE, 70, Dummy)

        result = field.parse(b"\x00\x00")
        self.assertEqual(result, Dummy.VALUE_0)

        result = field.parse(b"\x00\x01")
        self.assertEqual(result, Dummy.VALUE_1)

        result = field.parse(b"\x00\x02")
        self.assertEqual(result, Dummy.VALUE_2)

        result = field.parse(b"\x00\x03")
        self.assertIsNone(result)

    def test_is_writeable(self):
        field = SelectField(FieldName.AC_OUTPUT_MODE, 70, Dummy)
        self.assertTrue(field.is_writeable())

    def test_write_type_valid(self):
        field = SelectField(FieldName.AC_OUTPUT_MODE, 70, Dummy)
        self.assertTrue(field.allowed_write_type(Dummy.VALUE_1))

    def test_write_type_invalid(self):
        field = SelectField(FieldName.AC_OUTPUT_MODE, 70, Dummy)
        self.assertFalse(field.allowed_write_type(Dummy2.VALUE_3))
