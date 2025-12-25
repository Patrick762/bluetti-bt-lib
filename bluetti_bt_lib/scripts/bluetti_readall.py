import argparse
import asyncio
import json
import logging

from ..bluetooth.device_reader import DeviceReader, DeviceReaderConfig
from ..base_devices import BaseDeviceV1, BaseDeviceV2
from .types import ReadallData


async def async_read_device(address: str, iot_version: int, encryption: bool):
    device = None
    match iot_version:
        case 1:
            device = BaseDeviceV1()
        case 2:
            device = BaseDeviceV2()

    if device is None:
        print("Unknown iot protocol version")
        return

    reader = DeviceReader(
        address, device, asyncio.Future, DeviceReaderConfig(use_encryption=encryption)
    )

    print("Reader created")

    data = await reader.read(
        only_registers=device.get_full_registers_range(),
        raw=True,
    )

    if data is None:
        print("Error")
        return

    print("Writing data to file")

    register_data = {}
    for key, value in data.items():
        register_data[key] = value.hex()

    data_obj = ReadallData(
        address,
        iot_version,
        encryption,
        register_data,
    )

    with open(f"bluetti_data.{address.replace(':', '-')}.json", "w") as f:
        json.dump(data_obj.toJSON(), f)


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(description="Detect bluetti devices")
    parser.add_argument("-m", "--mac", type=str, help="Mac-address of the powerstation")
    parser.add_argument("-v", "--version", type=int, help="IoT protocol version")
    parser.add_argument(
        "-e", "--encryption", type=bool, help="Add this if encryption is needed"
    )
    args = parser.parse_args()

    if args.mac is None or args.version is None:
        parser.print_help()
        return

    encryption = False if args.encryption is None else True

    # logging.basicConfig(level=logging.DEBUG)

    asyncio.run(async_read_device(args.mac, args.version, encryption))
