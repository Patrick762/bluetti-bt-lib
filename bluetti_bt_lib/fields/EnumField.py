import struct
from enum import Enum
from typing import Any, Type, TypeVar

from . import DeviceField, FieldName


E = TypeVar("E", bound=Enum)


class EnumField(DeviceField):
    def __init__(self, name: FieldName, address: int, enum: Type[E]):
        super().__init__(name, address, 1)
        self.enum = enum

    def parse(self, data: bytes) -> E | None:
        val = struct.unpack("!H", data)[0]
        return self.enum(val)
