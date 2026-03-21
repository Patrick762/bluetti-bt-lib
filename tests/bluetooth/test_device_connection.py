import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock

from bluetti_bt_lib.bluetooth.device_connection import DeviceConnection


class MockClient:
    is_connected = True


class TestDeviceConnectionCallbacks(unittest.TestCase):
    def _conn(self) -> DeviceConnection:
        return DeviceConnection("AA:BB:CC:DD:EE:FF")

    def test_dispatch_data_calls_registered_callback(self):
        conn = self._conn()
        received = []
        conn.set_data_callback(received.append)
        conn._dispatch_data(b"\x01\x02")
        self.assertEqual(received, [b"\x01\x02"])

    def test_dispatch_data_without_callback_does_not_raise(self):
        conn = self._conn()
        conn._dispatch_data(b"\x01\x02")

    def test_clear_data_callback_stops_dispatch(self):
        conn = self._conn()
        received = []
        conn.set_data_callback(received.append)
        conn.clear_data_callback()
        conn._dispatch_data(b"\x01\x02")
        self.assertEqual(received, [])

    def test_replacing_callback_dispatches_to_new_one_only(self):
        conn = self._conn()
        first, second = [], []
        conn.set_data_callback(first.append)
        conn.set_data_callback(second.append)
        conn._dispatch_data(b"\xff")
        self.assertEqual(first, [])
        self.assertEqual(second, [b"\xff"])

    def test_dispatch_delivers_exact_bytes(self):
        conn = self._conn()
        received = []
        conn.set_data_callback(received.append)
        payload = bytes(range(20))
        conn._dispatch_data(payload)
        self.assertEqual(received[0], payload)


class TestDeviceConnectionIsConnected(unittest.TestCase):
    def test_is_connected_false_when_no_client(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        self.assertFalse(conn.is_connected)

    def test_is_connected_true_when_client_connected(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        conn._client = MockClient()
        self.assertTrue(conn.is_connected)

    def test_is_connected_false_when_client_reports_disconnected(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        client = MockClient()
        client.is_connected = False
        conn._client = client
        self.assertFalse(conn.is_connected)

    def test_address_property_returns_address(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        self.assertEqual(conn.address, "AA:BB:CC:DD:EE:FF")


class TestDeviceConnectionDisconnect(unittest.IsolatedAsyncioTestCase):
    async def test_disconnect_sets_client_to_none(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        conn._client = MockClient()
        conn._client.stop_notify = AsyncMock()
        conn._client.disconnect = AsyncMock()
        await conn.disconnect()
        self.assertIsNone(conn._client)

    async def test_disconnect_resets_encryption(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        conn._client = MockClient()
        conn._client.stop_notify = AsyncMock()
        conn._client.disconnect = AsyncMock()
        conn._encryption.reset = MagicMock()
        await conn.disconnect()
        conn._encryption.reset.assert_called_once()

    async def test_disconnect_when_no_client_does_not_raise(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        await conn.disconnect()  # should not raise


class TestDeviceConnectionEnsureConnected(unittest.IsolatedAsyncioTestCase):
    async def test_ensure_connected_skips_connect_when_already_connected(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        conn._client = MockClient()
        conn.connect = AsyncMock(side_effect=AssertionError("should not reconnect"))
        result = await conn.ensure_connected()
        self.assertTrue(result)

    async def test_ensure_connected_calls_connect_when_disconnected(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        conn.connect = AsyncMock(return_value=True)
        result = await conn.ensure_connected()
        conn.connect.assert_called_once()
        self.assertTrue(result)

    async def test_ensure_connected_returns_false_when_connect_fails(self):
        conn = DeviceConnection("AA:BB:CC:DD:EE:FF")
        conn.connect = AsyncMock(return_value=False)
        result = await conn.ensure_connected()
        self.assertFalse(result)
