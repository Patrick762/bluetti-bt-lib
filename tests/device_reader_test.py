import asyncio
import base64
import json
from pathlib import Path
from typing import TypedDict
import unittest

from bluetti_bt_lib.base_devices import BaseDeviceV1
from bluetti_bt_lib.bluetooth import DeviceReader, DeviceReaderConfig

from tests.bluetti_test_device import BluettiTestDevice

FIXTURES_DIR = Path(__file__).parent / "fixtures"
LOGGER_NAME = "bluetti_bt_lib.bluetooth.device_reader"


class DeviceFixture(TypedDict):
    readable_ranges: list[tuple[int, int]]
    writable_ranges: list[tuple[int, int]]
    data: list[tuple[int, str]]


def build_device(name: str, fixture_name: str) -> BluettiTestDevice:
    data: DeviceFixture = json.loads((FIXTURES_DIR / fixture_name).read_text())
    register_data = [(e[0], base64.b64decode(e[1])) for e in data["data"]]
    readable = [range(e[0], e[1]) for e in data["readable_ranges"]]
    writable = [range(e[0], e[1]) for e in data["writable_ranges"]]
    return BluettiTestDevice(name, register_data, readable, writable)


class TestDeviceReader(unittest.IsolatedAsyncioTestCase):
    async def test_v1_read(self):
        with build_device("AC3002139000462139", "ac300.json") as mock:
            reader = DeviceReader(
                mock.ble_device.address,
                BaseDeviceV1(),
                asyncio.get_running_loop().create_future,
                DeviceReaderConfig(1),
            )
            self.assertEqual(
                await reader.read(),
                {
                    "device_type": "AC300",
                    "device_sn": 2139000462139,
                    "total_battery_percent": 99,
                    "dc_input_power": 0,
                    "ac_input_power": 0,
                    "ac_output_power": 0,
                    "dc_output_power": 0,
                },
            )

    async def test_v1_read_raw(self):
        with build_device("AC3002139000462139", "ac300.json") as mock:
            reader = DeviceReader(
                mock.ble_device.address,
                BaseDeviceV1(),
                asyncio.get_running_loop().create_future,
                DeviceReaderConfig(1),
            )
            self.assertEqual(
                await reader.read(raw=True),
                {
                    10: b"AC300\x00\x00\x00\x00\x00\x00\x00",
                    17: b"\xdb;\x06\\\x01\xf2\x00\x00",
                    36: b"\x00\x00",
                    37: b"\x00\x00",
                    38: b"\x00\x00",
                    39: b"\x00\x00",
                    43: b"\x00c",
                },
            )

    async def test_v1_read_only(self):
        with build_device("AC3002139000462139", "ac300.json") as mock:
            device = BaseDeviceV1()
            reader = DeviceReader(
                mock.ble_device.address,
                device,
                asyncio.get_running_loop().create_future,
                DeviceReaderConfig(1),
            )
            parsed_data = await reader.read(
                only_registers=device.get_device_type_registers()
            )
            self.assertEqual(parsed_data, {"device_type": "AC300"})

    async def test_v1_connection_failure(self):
        with build_device("AC3002139000462139", "ac300.json") as mock:
            reader = DeviceReader(
                mock.ble_device.address,
                BaseDeviceV1(),
                asyncio.get_running_loop().create_future,
                DeviceReaderConfig(1),
            )
            with self.assertLogs(LOGGER_NAME) as cm:
                # The current code attempts 10 times, so we need that many failures
                mock.inject_connection_error(count=10)
                self.assertIsNone(await reader.read())
            self.assertEqual(cm.output, [f"WARNING:{LOGGER_NAME}:Timeout"])

    async def test_v1_does_not_check_response(self):
        with build_device("AC3002139000462139", "ac300.json") as mock:
            device = BaseDeviceV1()
            reader = DeviceReader(
                mock.ble_device.address,
                device,
                asyncio.get_running_loop().create_future,
                DeviceReaderConfig(1),
            )
            mock.override_next_response(b"\x01\x83\x02\xff\xff")
            self.assertEqual(
                await reader.read(
                    raw=True, only_registers=device.get_device_type_registers()
                ),
                {10: b""},
            )
