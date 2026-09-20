import struct

from . import DeviceField, FieldName


class UIntField(DeviceField):
    def __init__(
        self,
        name: FieldName,
        address: int,
        multiplier: float = 1,
        min: int | None = None,
        max: int | None = None,
    ):
        super().__init__(name, address, 1)
        self.multiplier = multiplier
        self.min = min
        self.max = max

    def parse(self, data: bytes) -> int:
        val = struct.unpack("!H", data)[0]
        if self.multiplier != 1:
            val = round(val * self.multiplier, 2)
        return val

    def in_range(self, value: int) -> bool:
        if self.min is not None and self.min > value:
            return False
        if self.max is not None and self.max < value:
            return False
        return value >= 0
