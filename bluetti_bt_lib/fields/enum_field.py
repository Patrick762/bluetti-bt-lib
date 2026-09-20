import struct
from enum import Enum
from typing import Type, TypeVar

from . import DeviceField, FieldName


E = TypeVar("E", bound=Enum)


class EnumField(DeviceField):
    def __init__(self, name: FieldName, address: int, e: Type[E]):
        super().__init__(name, address, 1)
        self.e = e

    def parse(self, data: bytes) -> E | None:
        val = struct.unpack("!H", data)[0]

        if val not in [e.value for e in self.e]:
            return None

        return self.e(val)
