import struct

from . import DeviceRegister, RegisterAction


class ReadableRegisters(DeviceRegister):
    def __init__(self, starting_address: int, quantity: int):
        super().__init__(
            RegisterAction.READ, struct.pack("!HH", starting_address, quantity)
        )
        self.starting_address = starting_address
        self.quantity = quantity

    def response_size(self) -> int:
        # 3 byte header
        # each returned field is actually 2 bytes (16-bit word)
        # 2 byte crc
        return 2 * self.quantity + 5

    def parse_response(self, response: bytes) -> bytes:
        return bytes(response[3:-2])

    def __repr__(self) -> str:
        return f"ReadableRegisters(starting_address={self.starting_address}, quantity={self.quantity})"
