import json
import argparse
import asyncio
import logging

from ..base_devices import BaseDeviceV1, BaseDeviceV2
from ..fields import FieldName, get_unit
from ..utils.device_builder import build_device
from .types import ReadallData


async def async_parse_file(filename: str):
    print(f"Reading file {filename}")

    with open(filename, "r") as json_data:
        dict_data = json.load(json_data)
        data = ReadallData(**dict_data)

    if data.iotVersion == 1:
        device = BaseDeviceV1()
    else:
        device = BaseDeviceV2()

    registers_map = bytearray(40000)

    registers: list[bytes] = [
        bytes.fromhex(b) if len(b) > 0 else b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        for b in data.registers.values()
    ]

    i = 0
    for r in registers:
        registers_map[i : i + 20] = r
        i += 20

    parsed = device.parse(1, registers_map, 0)

    device_type = parsed.get(FieldName.DEVICE_TYPE.value)

    if device_type is None:
        print("Unknown device type")
        print("Parsed data:", parsed)
        return

    device = build_device(device_type + "12345678")

    data = device.parse(1, registers_map, 0)

    print()
    for key, value in data.items():
        key = FieldName(key)
        unit = get_unit(key)
        print(f"{key}: {value}" + ("" if unit is None else unit))


def start():
    """Entrypoint."""
    parser = argparse.ArgumentParser(description="Parse readall output files")
    parser.add_argument(
        "file", type=str, help="JSON file of the powerstation readall output"
    )
    args = parser.parse_args()

    if args.file is None:
        parser.print_help()
        return

    logging.basicConfig(level=logging.WARNING)

    asyncio.run(async_parse_file(args.file))
