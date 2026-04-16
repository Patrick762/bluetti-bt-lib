"""Connect to Bluetti directly via Mac CoreBluetooth (no proxy)."""

import asyncio
import logging

from bleak import BleakClient, BleakScanner

from bluetti_bt_lib.const import NOTIFY_UUID, WRITE_UUID
from bluetti_bt_lib.registers import ReadableRegisters

# CoreBluetooth UUID (how Mac sees this device)
BLUETTI_CB_UUID = "A7108915-E5F4-F6E6-BA0B-2CFA96DF1397"
# Fallback: scan by name
BLUETTI_NAME = "SP200"


async def find_device():
    print("Scanning for Bluetti...")
    device = await BleakScanner.find_device_by_address(BLUETTI_CB_UUID, timeout=10.0)
    if device:
        print(f"Found by UUID: {device.address} ({device.name})")
        return device

    print("Not found by UUID, scanning by name...")
    device = await BleakScanner.find_device_by_filter(
        lambda d, _: d.name and "SP200" in d.name,
        timeout=10.0,
    )
    if device:
        print(f"Found by name: {device.address} ({device.name})")
    return device


async def run() -> None:
    device = await find_device()
    if device is None:
        print("Bluetti not found. Make sure Bluetooth is on and the device is nearby.")
        return

    print(f"Connecting to {device.address}...")
    async with BleakClient(device) as client:
        print(f"Connected! MTU: {client.mtu_size}")

        # List services
        for service in client.services:
            for char in service.characteristics:
                if char.uuid.lower() in (NOTIFY_UUID.lower(), WRITE_UUID.lower()):
                    print(f"  Found target char: {char.uuid} props={char.properties}")

        # Subscribe to notifications
        response_future: asyncio.Future[bytearray] = asyncio.get_event_loop().create_future()

        def on_notify(handle, data: bytearray) -> None:
            print(f"Notification: {data.hex()}")
            if not response_future.done():
                response_future.set_result(data)

        await client.start_notify(NOTIFY_UUID, on_notify)

        # Read device type (register 110, length 6)
        register = ReadableRegisters(110, 6)
        command = bytes(register)
        print(f"Sending command: {command.hex()}")
        await client.write_gatt_char(WRITE_UUID, command, response=False)

        print("Waiting for response...")
        try:
            data = await asyncio.wait_for(response_future, timeout=10)
            print(f"Raw: {data.hex()}")
            try:
                print(f"Decoded: {data[3:-2].decode('ascii').strip()}")
            except Exception:
                pass
        except asyncio.TimeoutError:
            print("Timed out waiting for response.")

        await client.stop_notify(NOTIFY_UUID)
    print("Done.")


logging.basicConfig(level=logging.WARNING)
asyncio.run(run())
