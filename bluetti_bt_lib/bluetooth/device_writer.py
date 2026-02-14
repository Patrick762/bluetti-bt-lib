import asyncio
import logging
from typing import Any
import async_timeout
from bleak import BleakClient
from bleak.exc import BleakError

from .encryption import BluettiEncryption, Message, MessageType
from ..const import NOTIFY_UUID, WRITE_UUID
from ..base_devices import BluettiDevice
from ..utils.privacy import mac_loggable


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
        self.has_notifier = False
        self.encryption = BluettiEncryption() if config.use_encryption else None

        self.logger = logging.getLogger(
            f"{__name__}.{mac_loggable(bleak_client.address).replace(':', '_')}"
        )

    def _notification_handler(self, _: int, data: bytearray):
        """Handle BLE notifications for encryption handshake (mirrors DeviceReader)."""
        if self.encryption is None:
            return
        message = Message(data)
        if message.is_pre_key_exchange:
            message.verify_checksum()
            if message.type == MessageType.CHALLENGE:
                response = self.encryption.msg_challenge(message)
                asyncio.create_task(
                    self.client.write_gatt_char(WRITE_UUID, response)
                )
                return
            if message.type == MessageType.CHALLENGE_ACCEPTED:
                self.logger.debug("Challenge accepted")
                return
        if self.encryption.unsecure_aes_key is None:
            return
        key, iv = self.encryption.getKeyIv()
        decrypted = Message(
            self.encryption.aes_decrypt(message.buffer, key, iv)
        )
        if decrypted.is_pre_key_exchange:
            decrypted.verify_checksum()
            if decrypted.type == MessageType.PEER_PUBKEY:
                response = self.encryption.msg_peer_pubkey(decrypted)
                asyncio.create_task(
                    self.client.write_gatt_char(WRITE_UUID, response)
                )
                return
            if decrypted.type == MessageType.PUBKEY_ACCEPTED:
                self.encryption.msg_key_accepted(decrypted)
                return

    async def write(self, field: str, value: Any):
        available_fields = [f.name for f in self.bluetti_device.fields]
        if field not in available_fields:
            self.logger.error("Field not supported")
            return

        command = self.bluetti_device.build_write_command(field, value)

        if command is None:
            self.logger.error("Field is not writeable")
            return

        self.logger.debug("Writing to device register")

        async with self.polling_lock:
            try:
                async with async_timeout.timeout(self.config.timeout):
                    if not self.client.is_connected:
                        self.logger.debug("Connecting to device")
                        await self.client.connect()

                    self.logger.debug("Connected to device")

                    if self.config.use_encryption:
                        if not self.has_notifier:
                            await self.client.start_notify(
                                NOTIFY_UUID, self._notification_handler
                            )
                            self.has_notifier = True
                        deadline = asyncio.get_running_loop().time() + 30
                        while not self.encryption.is_ready_for_commands:
                            if asyncio.get_running_loop().time() > deadline:
                                self.logger.error(
                                    "Encryption handshake timed out"
                                )
                                return
                            await asyncio.sleep(0.5)
                        command_bytes = self.encryption.aes_encrypt(
                            bytes(command),
                            self.encryption.secure_aes_key,
                            None,
                        )
                    else:
                        command_bytes = bytes(command)

                    self.logger.debug("Writing command")

                    await self.client.write_gatt_char(
                        WRITE_UUID,
                        command_bytes,
                    )

                    self.logger.debug("Write successful")

            except TimeoutError:
                self.logger.warning("Timeout")
                return None
            except BleakError as err:
                self.logger.warning("Bleak error: %s", err)
                return None
            except BaseException as err:
                self.logger.warning("Unknown error: %s", err)
                return None
            finally:
                await self.client.disconnect()
                self.logger.debug("Disconnected from device")
