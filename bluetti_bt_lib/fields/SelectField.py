import struct
from enum import Enum
from typing import Any, Type

from . import DeviceField, FieldName


class SelectField(DeviceField):
    def __init__(self, name: FieldName, address: int, enum: Type[Enum]):
        super().__init__(name, address, 1)
        self.enum = enum

    def parse(self, data: bytes) -> Any:
        val = struct.unpack("!H", data)[0]
        return self.enum(val)

    def is_writeable(self):
        return True

    def allowed_write_type(self, value: Any) -> bool:
        return isinstance(value, Type[Enum])
