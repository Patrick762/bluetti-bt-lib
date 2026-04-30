"""Subscribe to ESP32 logs while attempting BLE connection to Bluetti."""

import asyncio
import logging

from aioesphomeapi import APIClient, LogLevel

PROXY_ADDRESS = "192.168.178.41"
BLUETTI_MAC = "DC:B4:D9:51:F0:CA"
BLUETTI_ADDR = int(BLUETTI_MAC.replace(":", ""), 16)


async def run() -> None:
    cli = APIClient(address=PROXY_ADDRESS, port=6053, password=None, noise_psk=None)
    await cli.connect(login=True)
    info = await cli.device_info()
    feature_flags = info.bluetooth_proxy_feature_flags_compat(cli.api_version)
    print(f"Proxy: {info.name}  ESPHome: {info.esphome_version}  features: {feature_flags}")

    def on_log(msg) -> None:
        print(f"[ESP32] {msg.message}")

    cli.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_VERBOSE)

    connected = asyncio.Event()
    disconnected = asyncio.Event()

    def on_bt_state(is_connected: bool, mtu: int, error: int) -> None:
        print(f">>> BT state: connected={is_connected}  mtu={mtu}  error={error}")
        if is_connected:
            connected.set()
        else:
            disconnected.set()

    # Clear stale want_disconnect_ state from any previous session.
    # We must wait for the callback confirming it resolved before connecting.
    print("Clearing stale BLE state...")
    try:
        await cli.bluetooth_device_connect(
            BLUETTI_ADDR,
            on_bluetooth_connection_state=on_bt_state,
            timeout=5,
            feature_flags=feature_flags,
            has_cache=False,
            address_type=1,
        )
    except Exception as e:
        print(f"  (pre-connect raised: {e})")

    # Wait for a disconnect event (confirming the slot is clean) or just pause
    try:
        await asyncio.wait_for(disconnected.wait(), timeout=8)
        print("  Got disconnect confirmation, slot is clean.")
    except asyncio.TimeoutError:
        print("  No disconnect event received, proceeding anyway.")

    # Reset events for the real attempt
    connected.clear()
    disconnected.clear()
    await asyncio.sleep(1)

    print(f"Sending connect request to {BLUETTI_MAC}...")
    await cli.bluetooth_device_connect(
        BLUETTI_ADDR,
        on_bluetooth_connection_state=on_bt_state,
        timeout=10,
        feature_flags=feature_flags,
        has_cache=False,
        address_type=1,
    )

    try:
        await asyncio.wait_for(connected.wait(), timeout=10)
        print("Connected!")
    except asyncio.TimeoutError:
        print("Timed out waiting for connection.")

    await cli.disconnect()


logging.basicConfig(level=logging.WARNING)
asyncio.run(run())
