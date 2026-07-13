import struct

from . import FieldName
from .UIntField import UIntField


class IntField(UIntField):
    def parse(self, data: bytes) -> int:
        val = struct.unpack("!h", data)[0]
        if self.multiplier != 1:
            val = round(val * self.multiplier, 2)
        return val

    def in_range(self, value: int) -> bool:
        if self.min is not None and self.min > value:
            return False
        if self.max is not None and self.max < value:
            return False
        return True
