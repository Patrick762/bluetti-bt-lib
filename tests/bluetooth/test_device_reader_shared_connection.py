import asyncio
import struct
import unittest
from unittest.mock import AsyncMock

from bluetti_bt_lib.devices.ac180p import AC180P
from bluetti_bt_lib.bluetooth.device_reader import DeviceReader
from bluetti_bt_lib.fields import FieldName
from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption


class MockClientForSharedConnection(ClientMockNoEncryption):
    """Mock client that routes write responses directly to the DeviceConnection callback.

    In real BLE: write_gatt_char → notification → DeviceConnection._on_notification
                 → _dispatch_data → _data_callback (reader._on_data)
    Here we skip the notification layer since DeviceConnection is mocked out.
    """

    def __init__(self):
        super().__init__()
        self._data_callback = None

    async def write_gatt_char(self, char_specifier, data, response=None):
        cmd = struct.unpack_from("!HHHH", data)
        content = bytes(await self._get_register(cmd[1], cmd[2]))
        if self._data_callback is not None:
            self._data_callback(content)


class MockDeviceConnection:
    """Minimal DeviceConnection mock: wires reader's data callback to the mock client."""

    def __init__(self, client: MockClientForSharedConnection):
        self._client = client

    @property
    def client(self):
        return self._client

    @property
    def encryption(self):
        from bluetti_bt_lib.bluetooth.encryption import BluettiEncryption
        return BluettiEncryption()

    @property
    def is_connected(self):
        return True

    async def ensure_connected(self) -> bool:
        await asyncio.sleep(0)
        return True

    async def disconnect(self) -> None:
        await asyncio.sleep(0)  # mock — disconnect policy is tested separately

    def set_data_callback(self, callback):
        self._client._data_callback = callback

    def clear_data_callback(self):
        self._client._data_callback = None


class MockDeviceConnectionFailsToConnect(MockDeviceConnection):
    async def ensure_connected(self) -> bool:
        await asyncio.sleep(0)
        return False


def make_ac180p_client() -> MockClientForSharedConnection:
    client = MockClientForSharedConnection()
    client.add_r_int(142, 350)   # AC_OUTPUT_POWER
    client.add_r_int(140, 12)    # DC_OUTPUT_POWER
    client.add_r_int(144, 0)     # DC_INPUT_POWER
    client.add_r_int(146, 362)   # AC_INPUT_POWER
    client.add_r_int(1314, 2300) # AC_INPUT_VOLTAGE (DecimalField, divisor=1)
    return client


class TestDeviceReaderSharedConnectionNonEncrypted(unittest.IsolatedAsyncioTestCase):
    async def test_read_returns_ac180p_sensor_data(self):
        client = make_ac180p_client()
        connection = MockDeviceConnection(client)

        reader = DeviceReader(
            "AA:BB:CC:DD:EE:FF",
            AC180P(),
            asyncio.Future,
            connection=connection,
        )

        data = await reader.read()

        self.assertIsNotNone(data)
        self.assertEqual(data.get(FieldName.AC_OUTPUT_POWER.value), 350)
        self.assertEqual(data.get(FieldName.DC_OUTPUT_POWER.value), 12)
        self.assertEqual(data.get(FieldName.AC_INPUT_POWER.value), 362)

    async def test_read_clears_data_callback_after_read(self):
        client = make_ac180p_client()
        connection = MockDeviceConnection(client)

        reader = DeviceReader(
            "AA:BB:CC:DD:EE:FF",
            AC180P(),
            asyncio.Future,
            connection=connection,
        )

        await reader.read()

        self.assertIsNone(client._data_callback)

    async def test_read_returns_none_when_connection_fails(self):
        client = make_ac180p_client()
        connection = MockDeviceConnectionFailsToConnect(client)

        reader = DeviceReader(
            "AA:BB:CC:DD:EE:FF",
            AC180P(),
            asyncio.Future,
            connection=connection,
        )

        data = await reader.read()
        self.assertIsNone(data)

    async def test_multiple_reads_reuse_connection(self):
        client = make_ac180p_client()
        connection = MockDeviceConnection(client)
        connection.ensure_connected = AsyncMock(return_value=True)
        connection.disconnect = AsyncMock()

        reader = DeviceReader(
            "AA:BB:CC:DD:EE:FF",
            AC180P(),
            asyncio.Future,
            connection=connection,
        )

        await reader.read()
        await reader.read()

        self.assertEqual(connection.ensure_connected.call_count, 2)

    def test_callback_is_none_before_first_read(self):
        client = make_ac180p_client()
        connection = MockDeviceConnection(client)

        DeviceReader(
            "AA:BB:CC:DD:EE:FF",
            AC180P(),
            asyncio.Future,
            connection=connection,
        )

        self.assertIsNone(client._data_callback)
