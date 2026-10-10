import struct

from .UIntField import UIntField


class IntField(UIntField):
    """Signed variant of UIntField"""

    def parse(self, data: bytes) -> int:
        val = struct.unpack("!h", data)[0]
        if self.multiplier != 1:
            # Adding 0 turns the -0.0 of a negative multiplier into 0.0
            val = round(val * self.multiplier, 2) + 0
        return val

    def in_range(self, value: int) -> bool:
        if self.min is not None and self.min > value:
            return False
        if self.max is not None and self.max < value:
            return False
        return True
