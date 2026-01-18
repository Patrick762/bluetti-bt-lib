import struct

from . import DeviceField, FieldName


class BoolFieldNonZero(DeviceField):
    """Bool field where only value 1 means True.

    Used for devices like AC2P where ac_output_on register (2011) returns
    non-standard boolean values:
    - 1 = ON
    - 3 = OFF (device returns 3, not 0)

    This field treats only value 1 as True, any other value (including 3)
    is treated as False.
    """

    def __init__(self, name: FieldName, address: int):
        super().__init__(name, address, 1)

    def parse(self, data: bytes) -> bool:
        num = struct.unpack("!H", data)[0]
        return num == 1
