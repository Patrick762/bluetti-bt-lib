import struct

from . import DeviceRegister, RegisterAction


class WriteableRegister(DeviceRegister):
    def __init__(self, address: int, value: int):
        super().__init__(RegisterAction.WRITE, struct.pack("!HH", address, value))
        self.address = address
        self.value = value

    def response_size(self):
        return 8

    def parse_response(self, response: bytes):
        return bytes(response[4:6])

    def __repr__(self):
        return f"WriteableRegister(address={self.address}, value={self.value:#04x})"
