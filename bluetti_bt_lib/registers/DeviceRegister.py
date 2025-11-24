import struct
import crcmod.predefined
from enum import Enum

modbus_crc = crcmod.predefined.mkCrcFun("modbus")


class RegisterAction(Enum):
    READ = 3
    WRITE = 6


class DeviceRegister:
    def __init__(self, register_action: RegisterAction, data: bytes):
        self.register_action = register_action

        self.cmd = bytearray(len(data) + 4)
        self.cmd[0] = 1
        self.cmd[1] = register_action.value
        self.cmd[2:-2] = data
        struct.pack_into("<H", self.cmd, -2, modbus_crc(self.cmd[:-2]))

    def response_size(self) -> int:
        """Returns the expected response size in bytes"""
        raise NotImplementedError()

    def __iter__(self):
        """Provide an iter implemention so that bytes(cmd) works"""
        return iter(self.cmd)

    def is_exception_response(self, response: bytes):
        """Checks the response code to see if it's a MODBUS exception"""
        if len(response) < 2:
            return False
        else:
            return response[1] == self.register_action.value + 0x80

    def is_valid_response(self, response: bytes):
        """Validates that the reponse is complete and uncorrupted"""
        if len(response) < 3:
            return False

        crc = modbus_crc(response[0:-2])
        crc_bytes = crc.to_bytes(2, byteorder="little")
        return response[-2:] == crc_bytes

    def parse_response(self, response: bytes):
        """Returns the raw body of the response"""
        raise NotImplementedError()
