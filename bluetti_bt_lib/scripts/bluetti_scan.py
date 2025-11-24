"""Bluetti scan command."""

import argparse
import asyncio
from typing import List
from bleak import BleakScanner
from bleak.backends.device import BLEDevice

from ..utils.device_info import get_type_by_bt_name


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


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(
        description="Detect bluetti devices by bluetooth name"
    )
    parser.parse_args()

    asyncio.run(scan_async())
