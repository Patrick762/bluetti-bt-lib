"""Scan for any BLE devices via ESPHome proxy to validate the connection."""

import asyncio
import logging

import habluetooth
import bleak
from bleak_esphome import APIConnectionManager, ESPHomeDeviceConfig

PROXY_ADDRESS = "192.168.178.41"
CONNECTION_TIMEOUT = 15


async def run() -> None:
    esphome_device: ESPHomeDeviceConfig = {
        "address": PROXY_ADDRESS,
        "noise_psk": None,
    }
    conn = APIConnectionManager(esphome_device)

    await habluetooth.BluetoothManager().async_setup()

    print(f"Connecting to ESPHome proxy at {PROXY_ADDRESS}...")
    try:
        await asyncio.wait_for(conn.start(), timeout=CONNECTION_TIMEOUT)
    except asyncio.TimeoutError:
        print("Timed out connecting to proxy.")
        return

    print("Proxy connected. Scanning for 10s...")
    await asyncio.sleep(5)

    devices = await bleak.BleakScanner.discover(timeout=10, return_adv=True)

    if not devices:
        print("No BLE devices found.")
    else:
        print(f"\nFound {len(devices)} device(s):")
        for d, adv in devices.values():
            print(f"  {d.address}  RSSI={adv.rssi:>4}  {d.name or '(no name)'}")

    await conn.stop()


logging.basicConfig(level=logging.WARNING)
asyncio.run(run())
