import struct

from . import DeviceField, FieldName


class IntField(DeviceField):
    def __init__(self, name: FieldName, address: int):
        super().__init__(name, address, 1)

    def parse(self, data: bytes) -> int:
        return struct.unpack(">h", data)[0]
