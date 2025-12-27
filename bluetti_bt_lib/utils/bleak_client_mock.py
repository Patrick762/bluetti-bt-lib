"""Bleak Mock Client for unittests."""

import struct
import sys
from typing import Awaitable, Callable, Union
import uuid
from bleak.backends.characteristic import BleakGATTCharacteristic
import crcmod

if sys.version_info < (3, 12):
    from typing_extensions import Buffer
else:
    from collections.abc import Buffer

modbus_crc = crcmod.predefined.mkCrcFun("modbus")


class BleakClientMock:
    """Mock a BLE Client."""

    def __init__(self):
        self._bytemap: bytearray = bytearray(8000)

    def r_int(self, register: int, value: int):
        real = register * 2
        self._bytemap[real : real * 2] = struct.pack("!H", value)

    def r_str(self, register: int, value: str, max_size: int):
        real = register * 2
        self._bytemap[real : (real + max_size) * 2] = struct.pack(
            f"!{max_size}s", value.encode("ascii")
        )

    def r_sn(self, register: int, value: int):
        real = register * 2
        part4 = value & 0xFFFF
        part3 = (value >> 16) & 0xFFFF
        part2 = (value >> 32) & 0xFFFF
        part1 = (value >> 48) & 0xFFFF
        self._bytemap[real : real + 8] = struct.pack("!4H", part4, part3, part2, part1)

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
