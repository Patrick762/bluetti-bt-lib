import struct

from . import DeviceField, FieldName


class SerialNumberField(DeviceField):
    def __init__(self, name: FieldName, address: int):
        super().__init__(name, address, 4)

    def parse(self, data: bytes) -> str:
        values = struct.unpack("!4H", data)
        return values[0] + (values[1] << 16) + (values[2] << 32) + (values[3] << 48)
