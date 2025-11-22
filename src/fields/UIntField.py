import struct

from . import DeviceField


class UIntField(DeviceField):
    def __init__(self, name: str, address: int, multiplier: float = 1):
        super().__init__(name, address, 1)
        self.multiplier = multiplier

    def parse(self, data: bytes) -> int:
        val = struct.unpack("!H", data)[0]

        if self.multiplier != 1:
            val = round(val * self.multiplier, 2)

        return val
