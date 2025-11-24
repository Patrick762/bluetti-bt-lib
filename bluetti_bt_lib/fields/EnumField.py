import struct
from enum import Enum
from typing import Any, Type

from . import DeviceField, FieldName


class EnumField(DeviceField):
    def __init__(self, name: FieldName, address: int, enum: Type[Enum]):
        super().__init__(name, address, 1)
        self.enum = enum

    def parse(self, data: bytes) -> Any:
        val = struct.unpack("!H", data)[0]
        return self.enum(val)
