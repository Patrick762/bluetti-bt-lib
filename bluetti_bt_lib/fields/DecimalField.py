import struct
from decimal import Decimal

from . import DeviceField, FieldName


class DecimalField(DeviceField):
    def __init__(
        self, name: FieldName, address: int, scale: int = 1, multiplier: float = 1
    ):
        super().__init__(name, address, 1)
        self.scale = scale
        self.multiplier = multiplier

    def parse(self, data: bytes) -> Decimal:
        val = Decimal(struct.unpack("!H", data)[0])
        return (val / 10 ** self.scale) * Decimal(self.multiplier)
