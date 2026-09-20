import struct
from decimal import Decimal

from . import DeviceField, FieldName


class VersionField(DeviceField):
    def __init__(self, name: FieldName, address: int):
        super().__init__(name, address, 2)

    def parse(self, data: bytes) -> int | None:
        if len(data) != 4:
            return None

        values = struct.unpack("!2H", data)
        return Decimal(values[0] + (values[1] << 16)) / 100
