import struct

from . import DeviceField, FieldName


class BoolFieldNonZero(DeviceField):
    """Bool field where any non-zero value means True.
    
    Used for devices like AC2P where ac_output_on register (2011) returns
    non-standard values. The AC2P behavior is:
    - 0x0001 (1) = ON
    - 0x0003 (3) = also ON (non-standard value)
    - 0x0000 (0) = OFF
    
    This field treats any non-zero value as True, which correctly handles
    devices that return values other than 1 for the ON state.
    """
    def __init__(self, name: FieldName, address: int):
        super().__init__(name, address, 1)

    def parse(self, data: bytes) -> bool:
        num = struct.unpack("!H", data)[0]
        return num != 0