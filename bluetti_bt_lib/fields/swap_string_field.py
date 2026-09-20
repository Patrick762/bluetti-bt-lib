from . import DeviceField, FieldName


def swap_bytes(data: bytes):
    """Swaps the place of every other byte, returning a new byte array"""
    arr = bytearray(data)
    for i in range(0, len(arr) - 1, 2):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


class SwapStringField(DeviceField):
    def __init__(self, name: FieldName, address: int, size: int):
        super().__init__(name, address, size)

    def parse(self, data: bytes) -> str:
        return swap_bytes(data).rstrip(b"\0").decode("ascii", errors="ignore")
