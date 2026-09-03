import asyncio
import logging
from typing import Any

import async_timeout
from bleak import BleakClient
from bleak.exc import BleakError

from ..const import NOTIFY_UUID, WRITE_UUID
from ..base_devices import BluettiDevice
from ..utils.privacy import mac_loggable
from .encryption import BluettiEncryption, Message, MessageType


class DeviceWriterConfig:
    def __init__(self, timeout: int = 15, use_encryption: bool = False):
        self.timeout = timeout
        self.use_encryption = use_encryption


class DeviceWriter:
    def __init__(
        self,
        bleak_client: BleakClient,
        bluetti_device: BluettiDevice,
        config: DeviceWriterConfig = DeviceWriterConfig(),
        lock: asyncio.Lock = asyncio.Lock(),
    ):
        self.client = bleak_client
        self.bluetti_device = bluetti_device
        self.config = config
        self.polling_lock = lock
        self._encryption = BluettiEncryption()
        self.logger = logging.getLogger(
            f"{__name__}.{mac_loggable(bleak_client.address).replace(':', '_')}"
        )

    async def write(self, field: str, value: Any):
        command = self._build_write_command(field, value)
        if command is None:
            return

        async with self.polling_lock:
            try:
                async with async_timeout.timeout(self.config.timeout):
                    await self._connect_if_needed()
                    command_bytes = await self._prepare_command_bytes(bytes(command))
                    await self.client.write_gatt_char(WRITE_UUID, command_bytes)
                    self.logger.debug("Write successful")
            except TimeoutError:
                self.logger.warning("Timeout writing to device")
            except BleakError as err:
                self.logger.warning("Bleak error: %s", err)
            except Exception as err:
                self.logger.warning("Unknown error: %s", err)
            finally:
                await self._cleanup()

    def _build_write_command(self, field: str, value: Any):
        """Validate field and build the Modbus write command. Returns None if invalid."""
        if field not in [f.name for f in self.bluetti_device.fields]:
            self.logger.error("Field not supported: %s", field)
            return None
        command = self.bluetti_device.build_write_command(field, value)
        if command is None:
            self.logger.error("Field is not writeable: %s", field)
        return command

    async def _connect_if_needed(self):
        if not self.client.is_connected:
            self.logger.debug("Connecting to device")
            await self.client.connect()

    async def _prepare_command_bytes(self, raw_bytes: bytes) -> bytes:
        """Return command bytes ready to send: plain bytes or AES-encrypted after handshake."""
        if not self.config.use_encryption:
            return raw_bytes
        await self._complete_encryption_handshake()
        return self._encryption.aes_encrypt(raw_bytes, self._encryption.secure_aes_key, None)

    async def _complete_encryption_handshake(self):
        """Subscribe to BLE notifications and wait until ECDH key exchange is complete."""
        self._handshake_complete = asyncio.Event()
        await self.client.start_notify(NOTIFY_UUID, self._on_encryption_message)
        self.logger.debug("Waiting for encryption handshake...")
        try:
            await asyncio.wait_for(self._handshake_complete.wait(), timeout=12)
        except asyncio.TimeoutError:
            raise TimeoutError("Encryption handshake timed out")
        self.logger.debug("Encryption handshake complete")

    async def _cleanup(self):
        if self.config.use_encryption:
            try:
                await self.client.stop_notify(NOTIFY_UUID)
            except Exception:
                pass
            self._encryption.reset()
        try:
            await self.client.disconnect()
        except Exception:
            pass

    async def _on_encryption_message(self, _sender: int, data: bytearray):
        """Dispatch each BLE notification to the appropriate handshake handler."""
        message = Message(data)
        if message.is_pre_key_exchange:
            await self._handle_pre_key_message(message)
        else:
            await self._handle_encrypted_handshake_message(message)

    async def _handle_pre_key_message(self, message: Message):
        """Handle unencrypted handshake messages: challenge and challenge-accepted."""
        message.verify_checksum()
        if message.type == MessageType.CHALLENGE:
            self.logger.debug("Received challenge, sending response")
            response = self._encryption.msg_challenge(message)
            await self.client.write_gatt_char(WRITE_UUID, response)
        elif message.type == MessageType.CHALLENGE_ACCEPTED:
            self.logger.debug("Challenge accepted, starting key exchange")

    async def _handle_encrypted_handshake_message(self, message: Message):
        """Handle encrypted handshake messages: peer public key and key-accepted."""
        if self._encryption.unsecure_aes_key is None:
            self.logger.warning("Received encrypted message before challenge was completed")
            return

        key, iv = self._encryption.getKeyIv()
        decrypted = Message(self._encryption.aes_decrypt(message.buffer, key, iv))

        if not decrypted.is_pre_key_exchange:
            return

        decrypted.verify_checksum()
        if decrypted.type == MessageType.PEER_PUBKEY:
            self.logger.debug("Received peer public key, sending ours")
            response = self._encryption.msg_peer_pubkey(decrypted)
            await self.client.write_gatt_char(WRITE_UUID, response)
        elif decrypted.type == MessageType.PUBKEY_ACCEPTED:
            self.logger.debug("Key exchange complete, shared secret established")
            self._encryption.msg_key_accepted(decrypted)
            self._handshake_complete.set()
