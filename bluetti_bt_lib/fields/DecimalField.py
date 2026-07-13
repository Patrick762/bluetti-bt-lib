import struct
from decimal import Decimal

from . import DeviceField, FieldName


class DecimalField(DeviceField):
    def __init__(
        self,
        name: FieldName,
        address: int,
        scale: int = 1,
        multiplier: float = 1,
        min: Decimal | None = None,
        max: Decimal | None = None,
        precision: int | None = None,
    ):
        super().__init__(name, address, 1)
        self.scale = scale
        self.multiplier = multiplier
        self.min = min
        self.max = max
        self.precision = precision

    def parse(self, data: bytes) -> Decimal:
        val = Decimal(struct.unpack("!H", data)[0])
        result = (val / 10 ** self.scale) * Decimal(self.multiplier)
        if self.precision is not None:
            return round(result, self.precision)
        return result

    def in_range(self, value: Decimal) -> bool:
        if self.min is not None and self.min > value:
            return False
        if self.max is not None and self.max < value:
            return False
        return True
