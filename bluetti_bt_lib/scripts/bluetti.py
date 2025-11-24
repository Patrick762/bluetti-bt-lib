"""Bluetti BT commands."""

import asyncio
from typing import List
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice

from ..bluetooth import DeviceReader, DeviceReaderConfig
from ..bluetooth.device_recognizer import recognize_device
from ..utils.device_info import get_type_by_bt_name
from ..utils.device_builder import build_device


async def read_device(address: str):
    client = BleakClient(address)

    print("Detecting device type")
    print()

    recognized = await recognize_device(client, asyncio.Future)

    if recognized is None:
        print("Unable to find device type information")
        return

    print()
    print(
        "Device type is '{}' with iot version {}".format(
            recognized.name, recognized.iot_version
        )
    )
    print()

    built = build_device(recognized.name + "12345678")

    if built is None:
        print("Unsupported powerstation type")
        return

    print("Client created")

    reader = DeviceReader(
        client, built, asyncio.Future, DeviceReaderConfig(10, recognized.encrypted)
    )

    print("Reader created")

    data = await reader.read()

    if data is None:
        print("Error")
        return

    print()
    for key, value in data.items():
        print("{}: {}".format(key, value))
    print()


async def scan_async():
    stop_event = asyncio.Event()

    found: List[List[str]] = []

    async def callback(device: BLEDevice, _):
        result = get_type_by_bt_name(device.name)

        if result is not None or device.name.startswith("PBOX"):
            found.append(device.address)
            stop_event.set()
            print([result, device.address])

    async with BleakScanner(callback):
        await stop_event.wait()

    for dev in found:
        await read_device(dev)


def start():
    """Entrypoint."""
    asyncio.run(scan_async())

    print("done")
