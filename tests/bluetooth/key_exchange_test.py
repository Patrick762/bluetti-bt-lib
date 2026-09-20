import asyncio
import unittest

from bluetti_bt_lib import DeviceReader
from bluetti_bt_lib.base_devices import BaseDeviceV1
from bluetti_bt_lib.bluetooth.device_reader import DeviceReaderConfig
from bluetti_bt_lib.bluetooth.encryption import KEX_MAGIC, hexsum


class WriteCapturingClient:
    def __init__(self):
        self.writes = []

    async def write_gatt_char(self, uuid, data):
        self.writes.append(bytes(data))


def wrap_encrypted(encryption, body: bytes) -> bytes:
    plain = KEX_MAGIC + body + hexsum(body, 2)
    key, _ = encryption.getKeyIv()
    return encryption.aes_encrypt(plain, key, None)


class TestInBandKeyExchange(unittest.IsolatedAsyncioTestCase):
    def make_reader(self):
        reader = DeviceReader(
            "00:11:00:11:00:11",
            BaseDeviceV1(),
            asyncio.Future,
            config=DeviceReaderConfig(use_encryption=True),
        )
        reader.client = WriteCapturingClient()
        reader.encryption.unsecure_aes_key = bytes(16)
        reader.encryption.unsecure_aes_iv = bytes(16)
        reader.encryption.secure_aes_key = bytes(range(16))
        return reader

    async def test_challenge_inside_encrypted_channel_refreshes_iv(self):
        reader = self.make_reader()
        stale_iv = reader.encryption.unsecure_aes_iv
        frame = wrap_encrypted(reader.encryption, bytes([1, 4, 9, 8, 7, 6]))

        await reader._notification_handler(0, bytearray(frame))

        self.assertNotEqual(reader.encryption.unsecure_aes_iv, stale_iv)
        self.assertEqual(reader.notify_response, bytearray())
        self.assertEqual(len(reader.client.writes), 1)

    async def test_unknown_key_exchange_type_is_not_forwarded(self):
        reader = self.make_reader()
        frame = wrap_encrypted(reader.encryption, bytes([9, 4, 9, 8, 7, 6]))

        await reader._notification_handler(0, bytearray(frame))

        self.assertEqual(reader.notify_response, bytearray())
        self.assertEqual(reader.client.writes, [])
