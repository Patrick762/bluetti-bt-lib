"""Read Bluetti registers via ESPHome BLE proxy using aioesphomeapi directly."""

import asyncio
import logging

from aioesphomeapi import APIClient

from bluetti_bt_lib.const import NOTIFY_UUID, WRITE_UUID
from bluetti_bt_lib.registers import ReadableRegisters

PROXY_ADDRESS = "192.168.178.41"
BLUETTI_MAC = "DC:B4:D9:51:F0:CA"

# MAC as integer
BLUETTI_ADDR = int(BLUETTI_MAC.replace(":", ""), 16)


def find_handle(services, uuid: str) -> int | None:
    """Find GATT characteristic handle by UUID."""
    uuid = uuid.lower()
    for service in services.services:
        for char in service.characteristics:
            if char.uuid.lower() == uuid:
                return char.handle
    return None


async def run() -> None:
    cli = APIClient(address=PROXY_ADDRESS, port=6053, password=None, noise_psk=None)

    print(f"Connecting to ESPHome proxy at {PROXY_ADDRESS}...")
    await cli.connect(login=True)
    info = await cli.device_info()
    from aioesphomeapi import BluetoothProxyFeature
    feature_flags = info.bluetooth_proxy_feature_flags_compat(cli.api_version)
    print(f"Proxy: {info.name} (BT MAC: {info.bluetooth_mac_address})")
    print(f"BT proxy features: {feature_flags} → active={bool(feature_flags & BluetoothProxyFeature.ACTIVE_CONNECTIONS)}, caching={bool(feature_flags & BluetoothProxyFeature.REMOTE_CACHING)}")

    connected = asyncio.Event()
    disconnected = asyncio.Event()

    def on_bt_state(is_connected: bool, mtu: int, error: int) -> None:
        print(f"BT state: connected={is_connected}, mtu={mtu}, error={error}")
        if is_connected:
            connected.set()
        else:
            disconnected.set()

    # Clear any stale connection state from previous attempts
    try:
        await cli.bluetooth_device_disconnect(BLUETTI_ADDR)
        await asyncio.sleep(2)
    except Exception:
        pass

    print(f"Connecting to Bluetti ({BLUETTI_MAC})...")
    await cli.bluetooth_device_connect(
        BLUETTI_ADDR,
        on_bluetooth_connection_state=on_bt_state,
        timeout=60,
        feature_flags=feature_flags,
        address_type=1,
    )

    print("Waiting for BT connection...")
    await asyncio.wait_for(connected.wait(), timeout=60)
    print("Connected to Bluetti.")

    # Discover GATT services to get characteristic handles
    services = await cli.bluetooth_gatt_get_services(BLUETTI_ADDR)
    notify_handle = find_handle(services, NOTIFY_UUID)
    write_handle = find_handle(services, WRITE_UUID)

    print(f"NOTIFY handle: {notify_handle}  WRITE handle: {write_handle}")

    if notify_handle is None or write_handle is None:
        print("Could not find required GATT characteristics.")
        await cli.bluetooth_device_disconnect(BLUETTI_ADDR)
        await cli.disconnect()
        return

    # Set up notification handler
    response_future: asyncio.Future[bytearray] = asyncio.get_event_loop().create_future()

    def on_notify(handle: int, data: bytearray) -> None:
        print(f"Notification on handle {handle}: {data.hex()}")
        if not response_future.done():
            response_future.set_result(data)

    stop_notify, _ = await cli.bluetooth_gatt_start_notify(
        BLUETTI_ADDR, notify_handle, on_notify
    )

    # Read device type registers (110, length 6) — same as BaseDeviceV2
    register = ReadableRegisters(110, 6)
    command = bytes(register)
    print(f"Sending command: {command.hex()}")

    await cli.bluetooth_gatt_write(
        BLUETTI_ADDR, write_handle, command, response=False
    )

    print("Waiting for response...")
    try:
        data = await asyncio.wait_for(response_future, timeout=10)
        print(f"Raw response: {data.hex()}")
        # Decode as ASCII — device type is a string
        try:
            print(f"Decoded: {data[3:-2].decode('ascii').strip()}")
        except Exception:
            pass
    except asyncio.TimeoutError:
        print("Timed out waiting for response.")

    await stop_notify()
    await cli.bluetooth_device_disconnect(BLUETTI_ADDR)
    await cli.disconnect()
    print("Done.")


logging.basicConfig(level=logging.WARNING)
asyncio.run(run())
