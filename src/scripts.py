"""Bluetti BT commands."""

import asyncio
import logging
from typing import List
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice

from .bluetooth import DeviceReader, DeviceReaderConfig
from .utils.device_info import get_type_by_bt_name
from .utils.device_builder import build_device


async def read_device(name: str, address: str):
    built = build_device(address, name)

    if built is None:
        print("Unknown powerstation type")
        return

    client = BleakClient(address)

    print("Client created")

    reader = DeviceReader(client, built, asyncio.Future, DeviceReaderConfig(10, True))

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

        # TODO Handle PBOX IoT modules

        if result is not None:
            found.append(
                [
                    device.name,
                    device.address,
                ]
            )
            stop_event.set()
            print([result, device.address])

    async with BleakScanner(callback):
        await stop_event.wait()

    for dev in found:
        await read_device(dev[0], dev[1])


def start():
    """Entrypoint."""
    logging.basicConfig()

    asyncio.run(scan_async())

    print("done")
