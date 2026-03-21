import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock

from bluetti_bt_lib.devices.ac180p import AC180P
from bluetti_bt_lib.bluetooth.device_writer import DeviceWriter, DeviceWriterConfig
from bluetti_bt_lib.fields import FieldName
from bluetti_bt_lib.enums import ChargingMode


class MockClientForWrite:
    """Mock BleakClient that records write_gatt_char calls without processing them."""

    is_connected = True

    def __init__(self):
        self.written_data = []

    async def write_gatt_char(self, char_specifier, data, response=None):
        await asyncio.sleep(0)
        self.written_data.append(bytes(data))

    async def start_notify(self, char_specifier, callback, **kwargs):
        await asyncio.sleep(0)  # not needed — writer uses shared connection, no own notify subscription

    async def stop_notify(self, char_specifier):
        await asyncio.sleep(0)  # not needed — writer uses shared connection, no own notify subscription

    async def disconnect(self):
        await asyncio.sleep(0)  # not needed — mock, connection lifecycle managed by DeviceConnection


class MockDeviceConnection:
    def __init__(self, client: MockClientForWrite):
        self._client = client
        self._encryption = MagicMock()

    @property
    def client(self):
        return self._client

    @property
    def encryption(self):
        return self._encryption

    @property
    def address(self):
        return "AA:BB:CC:DD:EE:FF"

    @property
    def is_connected(self):
        return True

    async def ensure_connected(self) -> bool:
        await asyncio.sleep(0)
        return True

    async def disconnect(self) -> None:
        await asyncio.sleep(0)  # mock — disconnect policy is tested separately


class MockDeviceConnectionFailsToConnect(MockDeviceConnection):
    async def ensure_connected(self) -> bool:
        await asyncio.sleep(0)
        return False


class TestDeviceWriterSharedConnectionNonEncrypted(unittest.IsolatedAsyncioTestCase):
    def _make_writer(self, connection) -> DeviceWriter:
        return DeviceWriter(
            bleak_client=None,
            bluetti_device=AC180P(),
            config=DeviceWriterConfig(timeout=5, use_encryption=False),
            lock=asyncio.Lock(),
            connection=connection,
        )

    async def test_write_switch_field_sends_command(self):
        client = MockClientForWrite()
        connection = MockDeviceConnection(client)
        writer = self._make_writer(connection)

        await writer.write(FieldName.CTRL_AC.value, True)

        self.assertEqual(len(client.written_data), 1)

    async def test_write_switch_field_off_sends_command(self):
        client = MockClientForWrite()
        connection = MockDeviceConnection(client)
        writer = self._make_writer(connection)

        await writer.write(FieldName.CTRL_AC.value, False)

        self.assertEqual(len(client.written_data), 1)

    async def test_write_select_field_sends_command(self):
        client = MockClientForWrite()
        connection = MockDeviceConnection(client)
        writer = self._make_writer(connection)

        await writer.write(FieldName.CTRL_CHARGING_MODE.value, ChargingMode.STANDARD.name)

        self.assertEqual(len(client.written_data), 1)

    async def test_write_unknown_field_sends_nothing(self):
        client = MockClientForWrite()
        connection = MockDeviceConnection(client)
        writer = self._make_writer(connection)

        await writer.write("nonexistent_field", True)

        self.assertEqual(len(client.written_data), 0)

    async def test_write_read_only_field_sends_nothing(self):
        client = MockClientForWrite()
        connection = MockDeviceConnection(client)
        writer = self._make_writer(connection)

        # AC_OUTPUT_POWER is UIntField (read-only)
        await writer.write(FieldName.AC_OUTPUT_POWER.value, 100)

        self.assertEqual(len(client.written_data), 0)

    async def test_write_does_not_disconnect_shared_connection(self):
        client = MockClientForWrite()
        connection = MockDeviceConnection(client)
        connection.disconnect = AsyncMock()
        writer = self._make_writer(connection)

        await writer.write(FieldName.CTRL_AC.value, True)

        connection.disconnect.assert_not_called()

    async def test_write_calls_ensure_connected(self):
        client = MockClientForWrite()
        connection = MockDeviceConnection(client)
        connection.ensure_connected = AsyncMock(return_value=True)
        writer = self._make_writer(connection)

        await writer.write(FieldName.CTRL_AC.value, True)

        connection.ensure_connected.assert_called_once()
