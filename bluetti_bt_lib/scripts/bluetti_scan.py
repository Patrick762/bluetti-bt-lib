"""Bluetti scan command. Discovers devices by Bluetooth name; optional timeout for multi-device scan."""

import argparse
import asyncio
import logging
import re
from typing import Any, Dict, Optional

from bleak import BleakScanner
from bleak.backends.device import BLEDevice

from ..utils.device_info import get_type_by_bt_name


def _device_key(device: BLEDevice) -> str:
    """Normalised key for deduplication (case-insensitive)."""
    return (device.address or "").upper()


async def scan_async(
    timeout_seconds: Optional[float],
    name_filter: Optional[re.Pattern[str]],
) -> None:
    """Scan for Bluetti BLE devices. With timeout: scan N seconds and list all. Without: stop at first device."""
    found: Dict[str, dict] = {}
    stop_event = asyncio.Event()

    def callback(device: BLEDevice, advertisement_data: Any) -> None:
        device_type = get_type_by_bt_name(device.name)
        if device_type is None:
            return
        if name_filter is not None and device.name is not None:
            if not name_filter.search(device.name):
                return
        key = _device_key(device)
        if key in found:
            rssi = getattr(advertisement_data, "rssi", None)
            if rssi is not None and (found[key].get("rssi") is None or rssi > found[key]["rssi"]):
                found[key].update(name=device.name or "", rssi=rssi)
        else:
            found[key] = {
                "type": device_type,
                "address": device.address,
                "name": device.name or "",
                "rssi": getattr(advertisement_data, "rssi", None),
            }
        if timeout_seconds is None:
            stop_event.set()

    async with BleakScanner(callback):
        if timeout_seconds is not None:
            await asyncio.sleep(timeout_seconds)
        else:
            await stop_event.wait()

    for item in found.values():
        print([item["type"], item["address"]])


def start() -> None:
    """Entrypoint."""
    parser = argparse.ArgumentParser(
        description="Detect Bluetti devices by Bluetooth name"
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
    parser.add_argument(
        "-f",
        "--filter",
        type=str,
        default=None,
        metavar="REGEX",
        help="Only show devices whose Bluetooth name matches this regex",
    )
    args = parser.parse_args()

    name_filter = re.compile(args.filter) if args.filter else None

    logging.basicConfig(level=logging.WARNING)

    asyncio.run(
        scan_async(
            timeout_seconds=args.timeout,
            name_filter=name_filter,
        )
    )
