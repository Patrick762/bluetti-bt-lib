"""Bluetti scan command. Discovers devices by Bluetooth name; optional timeout for multi-device scan."""

import argparse
import asyncio
import logging
from typing import Optional, Set
from bleak import BleakScanner
from bleak.backends.device import BLEDevice

from ..utils.device_info import get_type_by_bt_name


async def scan_async(timeout_seconds: Optional[float] = None):
    """Scan for Bluetti devices. With timeout: scan N seconds and list all. Without: stop at first device."""
    stop_event = asyncio.Event()
    seen_addresses: Set[str] = set()  # deduplicate by address

    def device_key(device: BLEDevice) -> str:
        return (device.address or "").upper()

    async def callback(device: BLEDevice, _):
        result = get_type_by_bt_name(device.name)
        if result is None and not (device.name or "").startswith("PBOX"):
            return
        device_type = result if result is not None else "PBOX"
        addr = device_key(device)
        if addr in seen_addresses:
            return
        seen_addresses.add(addr)
        print([device_type, device.address])

        if timeout_seconds is None:
            stop_event.set()

    async with BleakScanner(callback):
        if timeout_seconds is not None:
            await asyncio.sleep(timeout_seconds)
        else:
            await stop_event.wait()


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(
        description="Detect bluetti devices by bluetooth name"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=None,
        metavar="SECONDS",
        help="Scan for this many seconds and list all discovered devices. "
        "If omitted, stop after the first device is found.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)

    asyncio.run(scan_async(timeout_seconds=args.timeout))
