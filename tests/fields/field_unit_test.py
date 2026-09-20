import unittest
from bluetti_bt_lib import get_unit, FieldName


class TestFieldUnit(unittest.TestCase):
    def test_field_with_unit(self):
        field = get_unit(FieldName.AC_1_I_V)
        self.assertIsNotNone(field)

    def test_field_without_unit(self):
        field = get_unit(FieldName.AC_O_SWITCH)
        self.assertIsNone(field)
