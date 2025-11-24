import struct
from typing import Any

from . import DeviceField, FieldName


class SwitchField(DeviceField):
    def __init__(self, name: FieldName, address: int):
        super().__init__(name, address, 1)

    def parse(self, data: bytes) -> bool:
        return struct.unpack("!H", data)[0] == 1

    def is_writeable(self):
        return True

    def allowed_write_type(self, value: Any) -> bool:
        return isinstance(value, bool)
