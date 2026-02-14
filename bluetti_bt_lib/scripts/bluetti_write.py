"""Bluetti write command."""

import argparse
import asyncio
import logging
from typing import Any
from bleak import BleakClient

from ..bluetooth import DeviceWriter, DeviceWriterConfig
from ..utils.device_builder import build_device


async def async_write(
    address: str, device_type: str, encryption: bool, field: str, value: Any
):
    built = build_device(device_type + "12345678")

    if built is None:
        print("Unsupported powerstation type")
        return

    config = DeviceWriterConfig(use_encryption=encryption)

    if encryption:
        writer = DeviceWriter(
            built,
            config,
            address=address,
            future_builder=asyncio.Future,
        )
        print("Writer created (encrypted)")
    else:
        client = BleakClient(address)
        writer = DeviceWriter(built, config, bleak_client=client)
        print("Writer created")

    ok = await writer.write(field, value)
    if ok:
        print("Write command sent successfully")
    else:
        print("Write failed")


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(description="Write to bluetti device")
    parser.add_argument("-m", "--mac", type=str, help="Mac-address of the powerstation")
    parser.add_argument(
        "-t", "--type", type=str, help="Type of the powerstation (AC70 f.ex.)"
    )
    parser.add_argument("--on", action="store_true", help="Set field on (true)")
    parser.add_argument("--off", action="store_true", help="Set field off (false)")
    parser.add_argument("-v", "--value", type=int, help="Value to write (integer)")
    parser.add_argument(
        "-s", "--select", type=str, help="Value to write to a Select/Enum field"
    )
    parser.add_argument(
        "-e", "--encryption", action="store_true", help="Use encryption (required for e.g. EL10, Handsfree 1)"
    )
    parser.add_argument("field", type=str, help="Field name (ctrl_ac, ctrl_dc, ctrl_power_lifting)")
    args = parser.parse_args()

    if args.mac is None or args.type is None or args.field is None:
        parser.print_help()
        return

    if not args.on and not args.off and args.value is None and args.select is None:
        parser.print_help()
        return

    value = args.on
    if args.off:
        value = False
    if args.value is not None:
        value = args.value
    if args.select is not None:
        value = args.select

    logging.basicConfig(level=logging.WARNING)

    asyncio.run(
        async_write(
            args.mac,
            args.type,
            args.encryption,
            args.field,
            value,
        )
    )


if __name__ == "__main__":
    start()
