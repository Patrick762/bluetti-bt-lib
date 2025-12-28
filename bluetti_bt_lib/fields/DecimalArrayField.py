from decimal import Decimal
import struct

from . import DeviceField


class DecimalArrayField(DeviceField):
    def __init__(self, name: str, address: int, size: int, scale: int):
        self.scale = scale
        super().__init__(name, address, size)

    def parse(self, data: bytes) -> Decimal:
        values = list(struct.unpack(f"!{self.size}H", data))
        return [Decimal(v) / 10 ** self.scale for v in values]
