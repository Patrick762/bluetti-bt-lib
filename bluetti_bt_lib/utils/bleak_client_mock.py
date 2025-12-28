"""Bleak Mock Client for unittests."""

from decimal import Decimal
import struct
import sys
from typing import Awaitable, Callable, List, Union
import uuid
from bleak.backends.characteristic import BleakGATTCharacteristic
import crcmod

if sys.version_info < (3, 12):
    from typing_extensions import Buffer
else:
    from collections.abc import Buffer

modbus_crc = crcmod.predefined.mkCrcFun("modbus")


def swap_bytes(data: bytes):
    """Swaps the place of every other byte, returning a new byte array"""
    arr = bytearray(data)
    for i in range(0, len(arr) - 1, 2):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


def r_int(value: int):
    return struct.pack("!H", value)


def r_str(value: str, max_size: int):
    return struct.pack(f"!{max_size}s", value.encode("ascii"))


def r_sstr(value: str, max_size: int):
    return swap_bytes(r_str(value, max_size))


def r_sn(value: int):
    part4 = value & 0xFFFF
    part3 = (value >> 16) & 0xFFFF
    part2 = (value >> 32) & 0xFFFF
    part1 = (value >> 48) & 0xFFFF
    return struct.pack("!4H", part4, part3, part2, part1)


class BleakClientMock:
    """Mock a BLE Client."""

    def __init__(self, packs_max: int = 0):
        self._bytemap: bytearray = bytearray(40000)
        self.packs: List[bytearray] = [bytearray() for _ in range(packs_max)]

    def add_r_int(self, register: int, value: int):
        real = register * 2
        self._bytemap[real : real + 2] = r_int(value)

    def add_r_str(self, register: int, value: str, max_size: int):
        real = register * 2
        self._bytemap[real : real + max_size * 2] = r_str(value, max_size)

    def add_r_sstr(self, register: int, value: str, max_size: int):
        real = register * 2
        self._bytemap[real : real + max_size * 2] = r_sstr(value, max_size)

    def add_r_sn(self, register: int, value: int):
        real = register * 2
        self._bytemap[real : real + 8] = r_sn(value)

    def add_pack(self, n: int, b: bytearray):
        self.packs[n] = b

    async def start_notify(
        self,
        char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID],
        callback: Callable[
            [BleakGATTCharacteristic, bytearray], Union[None, Awaitable[None]]
        ],
        **kwargs,
    ) -> None:
        self._callback = callback

    async def stop_notify(
        self,
        char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID],
    ) -> None:
        return

    async def disconnect(self) -> None:
        return

    async def write_gatt_char(
        self,
        char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID],
        data: Buffer,
        response: bool = None,
    ) -> None:
        cmd = struct.unpack_from("!HHHH", data)
        content = await self._get_register(cmd[1], cmd[2])
        await self._callback(char_specifier, content)

    async def _get_register(self, addr: int, size: int):
        data = self._bytemap[(addr * 2) : (addr * 2 + size * 2)]
        response = bytearray(len(data) + 4)
        response[0] = 0
        response[1] = 0
        response[2] = 0
        response[3:-2] = data
        struct.pack_into("<H", response, -2, modbus_crc(response[:-2]))
        return response


class ClientMockNoEncryption(BleakClientMock):
    """Mock for unencrypted devices"""
