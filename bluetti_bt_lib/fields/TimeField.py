import struct
from decimal import Decimal

from . import DeviceField, FieldName


class TimeField(DeviceField):
    def __init__(
        self,
        name: FieldName,
        address: int,
    ):
        super().__init__(name, address, 1)

    def parse(self, data: bytes) -> Decimal:
        # TODO
        val = Decimal(struct.unpack("!H", data)[0])
        return (val / 10**self.scale) * Decimal(self.multiplier)
