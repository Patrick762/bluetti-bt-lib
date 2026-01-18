import struct

from bluetti_bt_lib.fields import BoolFieldNonZero, FieldName


class TestBoolFieldNonZero:
    def test_parse_zero_returns_false(self):
        field = BoolFieldNonZero(FieldName.AC_OUTPUT_ON, 2011)
        data = struct.pack("!H", 0)
        assert field.parse(data) is False

    def test_parse_one_returns_true(self):
        field = BoolFieldNonZero(FieldName.AC_OUTPUT_ON, 2011)
        data = struct.pack("!H", 1)
        assert field.parse(data) is True

    def test_parse_three_returns_false(self):
        """AC2P returns value 3 for OFF state (not 0)."""
        field = BoolFieldNonZero(FieldName.AC_OUTPUT_ON, 2011)
        data = struct.pack("!H", 3)
        assert field.parse(data) is False

    def test_parse_other_values_return_false(self):
        """Only value 1 should return True."""
        field = BoolFieldNonZero(FieldName.AC_OUTPUT_ON, 2011)
        for value in [2, 5, 100, 255, 65535]:
            data = struct.pack("!H", value)
            assert field.parse(data) is False

    def test_address(self):
        field = BoolFieldNonZero(FieldName.AC_OUTPUT_ON, 2011)
        assert field.address == 2011

    def test_size(self):
        field = BoolFieldNonZero(FieldName.AC_OUTPUT_ON, 2011)
        assert field.size == 1

    def test_name(self):
        field = BoolFieldNonZero(FieldName.AC_OUTPUT_ON, 2011)
        assert field.name == FieldName.AC_OUTPUT_ON.value
