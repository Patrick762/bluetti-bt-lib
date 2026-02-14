import asyncio
import logging
from typing import Any, Callable, Optional
import async_timeout
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from .encryption import BluettiEncryption, Message, MessageType
from ..const import NOTIFY_UUID, WRITE_UUID
from ..base_devices import BluettiDevice
from ..registers import WriteableRegister
from ..utils.privacy import mac_loggable


class DeviceWriterConfig:
    def __init__(self, timeout: int = 15, use_encryption: bool = False):
        self.timeout = timeout
        self.use_encryption = use_encryption


class DeviceWriter:
    def __init__(
        self,
        bluetti_device: BluettiDevice,
        config: DeviceWriterConfig = DeviceWriterConfig(),
        lock: asyncio.Lock = asyncio.Lock(),
        bleak_client: Optional[BleakClient] = None,
        address: Optional[str] = None,
        future_builder: Optional[Callable[[], asyncio.Future[Any]]] = None,
    ):
        self.bluetti_device = bluetti_device
        self.config = config
        self.polling_lock = lock
        self.client = bleak_client
        self.address = address
        self.create_future = future_builder

        log_id = mac_loggable(address or (bleak_client.address if bleak_client else "?"))
        self.logger = logging.getLogger(f"{__name__}.{log_id.replace(':', '_')}")

        self.encryption = BluettiEncryption() if config.use_encryption else None

    async def _notification_handler(self, _: int, data: bytearray) -> None:
        """Handle BLE notifications for encryption handshake (same logic as reader)."""
        if not self.config.use_encryption or not self.encryption:
            return
        message = Message(data)
        if message.is_pre_key_exchange:
            message.verify_checksum()
            if message.type == MessageType.CHALLENGE:
                response = self.encryption.msg_challenge(message)
                if response and self.client:
                    await self.client.write_gatt_char(WRITE_UUID, response)
                return
            if message.type == MessageType.CHALLENGE_ACCEPTED:
                self.logger.debug("Challenge accepted")
                return
        if self.encryption.unsecure_aes_key is None:
            self.logger.error("Received encrypted message before key initialization")
            return
        key, iv = self.encryption.getKeyIv()
        decrypted = Message(self.encryption.aes_decrypt(message.buffer, key, iv))
        if decrypted.is_pre_key_exchange:
            decrypted.verify_checksum()
            if decrypted.type == MessageType.PEER_PUBKEY:
                response = self.encryption.msg_peer_pubkey(decrypted)
                if response and self.client:
                    await self.client.write_gatt_char(WRITE_UUID, response)
                return
            if decrypted.type == MessageType.PUBKEY_ACCEPTED:
                self.encryption.msg_key_accepted(decrypted)
                return

    async def write(self, field: str, value: Any) -> bool:
        available_fields = [f.name for f in self.bluetti_device.fields]
        if field not in available_fields:
            self.logger.error("Field not supported")
            return False

        command = self.bluetti_device.build_write_command(field, value)
        if command is None:
            self.logger.error("Field is not writeable")
            return False

        if self.config.use_encryption and self.address and self.create_future:
            return await self._write_encrypted(command)
        if self.client:
            return await self._write_plain(command)
        self.logger.error("No client or address for write")
        return False

    async def _write_plain(self, command: WriteableRegister) -> bool:
        async with self.polling_lock:
            try:
                async with async_timeout.timeout(self.config.timeout):
                    if not self.client.is_connected:
                        await self.client.connect()
                    await self.client.write_gatt_char(WRITE_UUID, bytes(command))
                    self.logger.debug("Write successful")
                    return True
            except (TimeoutError, BleakError, BaseException) as err:
                self.logger.warning("Write failed: %s", err)
                return False
            finally:
                if self.client:
                    await self.client.disconnect()

    async def _write_encrypted(self, command: WriteableRegister) -> bool:
        async with self.polling_lock:
            try:
                async with async_timeout.timeout(self.config.timeout):
                    self.logger.debug("Searching for device")
                    device = await BleakScanner.find_device_by_address(
                        self.address, timeout=5
                    )
                    if device is None:
                        self.logger.error("Device not found")
                        return False
                    self.logger.debug("Connecting to device")
                    self.client = await establish_connection(
                        BleakClientWithServiceCache,
                        device,
                        device.name or "Unknown Device",
                        max_attempts=10,
                    )
                    await self.client.start_notify(
                        NOTIFY_UUID, self._notification_handler
                    )
                    while not self.encryption.is_ready_for_commands:
                        await asyncio.sleep(0.5)
                    command_bytes = self.encryption.aes_encrypt(
                        bytes(command),
                        self.encryption.secure_aes_key,
                        None,
                    )
                    await self.client.write_gatt_char(WRITE_UUID, command_bytes)
                    self.logger.debug("Write successful")
                    await asyncio.sleep(0.5)
                    return True
            except (TimeoutError, BleakError, BaseException) as err:
                self.logger.warning("Write failed: %s", err)
                return False
            finally:
                if self.encryption:
                    self.encryption.reset()
                if self.client:
                    try:
                        await self.client.stop_notify(NOTIFY_UUID)
                    except Exception:
                        pass
                    await self.client.disconnect()
                    self.client = None
