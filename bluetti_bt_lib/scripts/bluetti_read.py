"""Bluetti read command."""

import argparse
import asyncio
import logging

from ..bluetooth.device_reader import DeviceReader, DeviceReaderConfig
from ..utils.device_builder import build_device
from ..fields import FieldName, get_unit


async def async_read_device(address: str, type: str, encryption: bool):
    built = build_device(type + "12345678")

    if built is None:
        print("Unsupported powerstation type")
        return

    print("Client created")

    reader = DeviceReader(
        address, built, asyncio.Future, DeviceReaderConfig(use_encryption=encryption)
    )

    print("Reader created")

    data = await reader.read()

    if data is None:
        print("Error")
        return

    print()
    for key, value in data.items():
        key = FieldName(key) if key in [i.value for i in FieldName] else key
        unit = get_unit(key)
        print(f"{key}: {value}" + ("" if unit is None else unit))


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(description="Detect bluetti devices")
    parser.add_argument("-m", "--mac", type=str, help="Mac-address of the powerstation")
    parser.add_argument(
        "-t", "--type", type=str, help="Type of the powerstation (AC70 f.ex.)"
    )
    parser.add_argument(
        "-e", "--encryption", type=bool, help="Add this if encryption is needed"
    )
    args = parser.parse_args()

    if args.mac is None or args.type is None:
        parser.print_help()
        return

    logging.basicConfig(level=logging.WARNING)

    asyncio.run(async_read_device(args.mac, args.type, args.encryption))
