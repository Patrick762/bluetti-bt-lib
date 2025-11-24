import struct

from . import DeviceField, FieldName


class BoolField(DeviceField):
    def __init__(self, name: FieldName, address: int):
        super().__init__(name, address, 1)

    def parse(self, data: bytes) -> bool:
        return struct.unpack("!H", data)[0] == 1
