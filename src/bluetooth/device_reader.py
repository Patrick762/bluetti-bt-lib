import asyncio
import logging
import async_timeout
from typing import Any, Callable, List, cast
from bleak import BleakClient
from bleak.exc import BleakError

from .encryption import BluettiEncryption, Message, MessageType
from ..registers import ReadableRegisters
from ..const import NOTIFY_UUID, WRITE_UUID
from ..base_devices import BluettiDevice

_LOGGER = logging.getLogger(__name__)


class DeviceReaderConfig:
    def __init__(self, timeout: int = 60, use_encryption: bool = False):
        self.timeout = timeout
        self.use_encryption = use_encryption


class DeviceReader:
    def __init__(
        self,
        bleak_client: BleakClient,
        bluetti_device: BluettiDevice,
        future_builder_method: Callable[[], asyncio.Future[Any]],
        config: DeviceReaderConfig | None = None,
    ):
        self.client = bleak_client
        self.bluetti_device = bluetti_device
        self.create_future = future_builder_method

        if config is not None:
            self.config = config
        else:
            self.config = DeviceReaderConfig()

        self.has_notifier = False
        self.current_registers = None
        self.notify_response = bytearray()
        self.notify_future: asyncio.Future[Any] | None = None
        self.encryption = BluettiEncryption()
        self.polling_lock = asyncio.Lock()

    async def read(
        self, only_registers: List[ReadableRegisters] | None = None
    ) -> dict | None:
        registers = self.bluetti_device.get_polling_registers()

        if only_registers is not None:
            registers = only_registers

        parsed_data: dict = {}

        _LOGGER.debug("Reading device registers")

        async with self.polling_lock:
            try:
                async with async_timeout.timeout(self.config.timeout):
                    if not self.client.is_connected:
                        _LOGGER.debug("Connecting to device")
                        await self.client.connect()

                    _LOGGER.debug("Connected to device")

                    if not self.has_notifier:
                        await self.client.start_notify(
                            NOTIFY_UUID, self._notification_handler
                        )
                        self.has_notifier = True

                    _LOGGER.debug("Notification handler setup complete")

                    while (
                        self.config.use_encryption
                        and not self.encryption.is_ready_for_commands
                    ):
                        await asyncio.sleep(5)
                        _LOGGER.debug("Encryption handshake not finished yet")

                    for register in registers:
                        body = register.parse_response(
                            await self._async_send_command(register)
                        )

                        _LOGGER.debug("Raw data: %s", body)

                        parsed = self.bluetti_device.parse(
                            register.starting_address, body
                        )

                        _LOGGER.debug("Parsed data: %s", parsed)

                        parsed_data.update(parsed)

            except TimeoutError:
                _LOGGER.warning("Timeout")
                return None
            except BleakError as err:
                _LOGGER.warning("Bleak error: %s", err)
                return None
            except BaseException as err:
                _LOGGER.warning("Unknown error: %s", err)
                return None
            finally:
                if self.has_notifier:
                    try:
                        await self.client.stop_notify(NOTIFY_UUID)
                        _LOGGER.debug("Stopped notifier")
                    except:
                        # Ignore errors here
                        pass
                    self.has_notifier = False
                await self.client.disconnect()
                _LOGGER.debug("Disconnected from device")

            # Reset Encryption keys
            self.encryption.reset()

            # Check if dict is empty
            if not parsed_data:
                return None

            return parsed_data

    async def _async_send_command(self, registers: ReadableRegisters) -> bytes:
        """Send command and return response"""
        self.current_registers = registers
        self.notify_response = bytearray()
        self.notify_future = self.create_future()

        command_bytes = bytes(registers)

        # Encrypt command
        if self.config.use_encryption is True:
            if not self.encryption.is_ready_for_commands:
                return bytes()
            command_bytes = self.encryption.aes_encrypt(
                command_bytes, self.encryption.secure_aes_key, None
            )

        try:
            # Make request
            await self.client.write_gatt_char(WRITE_UUID, command_bytes)

            _LOGGER.debug("Request sent (%s)", registers)

            # Wait for response
            res = await asyncio.wait_for(self.notify_future, timeout=5)

            _LOGGER.debug("Got response")

            return cast(bytes, res)
        except:
            _LOGGER.warning("Error while reading data")

        return bytes()

    async def _notification_handler(self, _: int, data: bytearray):
        """Handle bt data."""
        _LOGGER.debug("Got new data")

        if self.config.use_encryption is True:
            message = Message(data)

            if message.is_pre_key_exchange:
                message.verify_checksum()

                if message.type == MessageType.CHALLENGE:
                    challenge_response = self.encryption.msg_challenge(message)
                    await self.client.write_gatt_char(WRITE_UUID, challenge_response)
                    return

                if message.type == MessageType.CHALLENGE_ACCEPTED:
                    _LOGGER.debug("Challenge accepted")
                    return

            if self.encryption.unsecure_aes_key is None:
                _LOGGER.error("Received encrypted message before key initialization")

            key, iv = self.encryption.getKeyIv()
            decrypted = Message(self.encryption.aes_decrypt(message.buffer, key, iv))

            if decrypted.is_pre_key_exchange:
                decrypted.verify_checksum()

                if decrypted.type == MessageType.PEER_PUBKEY:
                    peer_pubkey_response = self.encryption.msg_peer_pubkey(decrypted)
                    await self.client.write_gatt_char(WRITE_UUID, peer_pubkey_response)
                    return

                if decrypted.type == MessageType.PUBKEY_ACCEPTED:
                    self.encryption.msg_key_accepted(decrypted)
                    return

            # Handle as message
            data = decrypted.buffer

        # Save data
        self.notify_response.extend(data)
        self.notify_future.set_result(self.notify_response)
