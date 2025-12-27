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

    registers: list[bytes] = [bytes.fromhex(b) for b in data.registers.values()]

    parsed = {}

    addr = 1
    for r in registers:
        parsed.update(device.parse(addr, r, 0))
        addr += 50

    device_type = parsed.get(FieldName.DEVICE_TYPE.value)

    device = build_device(device_type + "12345678")

    data = {}

    addr = 1
    for r in registers:
        data.update(device.parse(addr, r))
        addr += 50

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
