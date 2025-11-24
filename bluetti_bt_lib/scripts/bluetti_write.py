"""Bluetti write command."""

import argparse
import asyncio
from typing import Any
from bleak import BleakClient

from ..bluetooth import DeviceWriter
from ..utils.device_builder import build_device


async def async_write(
    address: str, type: str, encryption: bool, field: str, value: Any
):
    client = BleakClient(address)
    built = build_device(type + "12345678")

    if built is None:
        print("Unsupported powerstation type")
        return

    if encryption:
        print("Encryption is not supported")
        return

    print("Client created")

    writer = DeviceWriter(
        client,
        built,
    )

    print("Writer created")

    await writer.write(field, value)


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(description="Write to bluetti device")
    parser.add_argument("-m", "--mac", type=str, help="Mac-address of the powerstation")
    parser.add_argument(
        "-t", "--type", type=str, help="Type of the powerstation (AC70 f.ex.)"
    )
    parser.add_argument("--on", type=bool, help="Value to write")
    parser.add_argument("--off", type=bool, help="Value to write")
    parser.add_argument("-v", "--value", type=int, help="Value to write")
    parser.add_argument(
        "-e", "--encryption", type=bool, help="Add this if encryption is needed"
    )
    parser.add_argument("field", type=str, help="Field name (ctrl_dc f.ex.)")
    args = parser.parse_args()

    if args.mac is None or args.type is None or args.field is None:
        parser.print_help()
        return

    # No value given
    if args.on is None and args.off is None and args.value is None:
        parser.print_help()
        return

    value = args.on is not None
    if args.off is not None:
        value = False

    if args.value:
        value = args.value

    asyncio.run(
        async_write(
            args.mac,
            args.type,
            args.encryption,
            args.field,
            value,
        )
    )
