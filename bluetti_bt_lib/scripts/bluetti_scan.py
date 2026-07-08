"""Bluetti scan command."""

import argparse
import asyncio
import logging
import re
from typing import List
from bleak import BleakScanner
from bleak.backends.device import BLEDevice

from ..utils.device_info import get_type_by_bt_name


async def scan_async(custom_regex, scan_time):
    # maybe there is some other trigger we would want to stop scan on?
    stop_event = asyncio.Event()
    # We can set the above event to prematurely stop the scan e.g. with `stop_event.set()`

    found: List[List[str]] = []

    print(f"Scanning for {scan_time} seconds (or until Ctrl+C)...")

    async def callback(device: BLEDevice, _):
        if device.name is None:
            return

        if custom_regex:
            match = re.match(custom_regex, device.name)
            result = None if match is None else match[0]
        else:
            result = get_type_by_bt_name(device.name)

        if result is not None or device.name.startswith("PBOX"):
            if not any(device.address in devices for devices in found):
                found.append(device.address)
                print([result, device.address])

    async with BleakScanner(callback):
        try:
            await asyncio.wait_for(stop_event.wait(), scan_time)
        except (asyncio.exceptions.CancelledError, asyncio.TimeoutError):
            exit()


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(
        description="Detect bluetti devices by bluetooth name"
    )
    parser.add_argument(
        "-r", "--regex", type=str, help="Custom regex to match device name"
    )
    parser.add_argument(
        "-s",
        "--scan-time",
        type=int,
        default=5,
        help="How long to scan for devices (seconds)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)

    asyncio.run(scan_async(args.regex, args.scan_time))


if __name__ == "__main__":
    start()
