import asyncio
from enum import Enum
import logging
from typing import Any, Callable, cast
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from .encryption import BluettiEncryption, Message, MessageType, AES_BLOCK_SIZE
from ..base_devices import BluettiDevice
from ..const import NOTIFY_UUID, WRITE_UUID
from ..registers import ReadableRegisters, DeviceRegister
from ..utils.privacy import mac_loggable


class DeviceReaderConfig:
    def __init__(self, timeout: int = 60, use_encryption: bool = False):
        self.timeout = timeout
        self.use_encryption = use_encryption


class DeviceReader:
    def __init__(
        self,
        mac: str,
        bluetti_device: BluettiDevice,
        future_builder_method: Callable[[], asyncio.Future[Any]],
        config: DeviceReaderConfig = DeviceReaderConfig(),
        lock: asyncio.Lock = asyncio.Lock(),
        ble_device: BLEDevice | None = None,
        ble_client: BleakClient | None = None,
    ):
        self.mac = mac
        self.bluetti_device = bluetti_device
        self.create_future = future_builder_method
        self.config = config
        self.polling_lock = lock
        self.ble_device = ble_device
        self.ble_client = ble_client

        self.logger = logging.getLogger(
            f"{__name__}.{mac_loggable(mac).replace(':', '_')}"
        )

        self.device: BLEDevice | None = None
        self.client: BleakClient | None = None

        self.has_notifier = False
        self.current_registers: DeviceRegister | None = None
        self.notify_response = bytearray()
        self.notify_future: asyncio.Future[Any] | None = None
        self.encryption = BluettiEncryption()
        self.encrypted_buffer = bytearray()

    async def read(
        self, only_registers: list[ReadableRegisters] | None = None, raw: bool = False
    ) -> dict[str, bool | int | float | Enum | str | bytes] | None:

        registers = self.bluetti_device.get_polling_registers()
        pack_registers = self.bluetti_device.get_pack_polling_registers()

        if only_registers is not None:
            registers = only_registers
            pack_registers = []

        parsed_data: dict[str, bool | int | float | Enum | str | bytes] = {}

        self.logger.debug("Reading device registers")

        async with self.polling_lock:
            try:
                async with asyncio.timeout(self.config.timeout):
                    self.logger.debug("Searching for device")

                    if self.ble_client:
                        self.device = None
                    elif self.ble_device is not None:
                        self.device = self.ble_device
                    else:
                        self.device = await BleakScanner.find_device_by_address(
                            self.mac, timeout=5
                        )

                        if self.device is None:
                            self.logger.debug("Device not found")
                            return None

                    self.logger.debug("Connecting to device")

                    if self.ble_client:
                        self.client = self.ble_client
                    else:
                        if self.device is None:
                            self.logger.debug("Device, Client or mac have to be set")
                            return None

                        self.client = await establish_connection(
                            BleakClientWithServiceCache,
                            self.device,
                            self.device.name or "Unknown Device",
                            max_attempts=10,
                        )

                    self.logger.debug("Connected to device")

                    if not self.has_notifier:
                        await self.client.start_notify(
                            NOTIFY_UUID, self._notification_handler
                        )
                        self.has_notifier = True

                    self.logger.debug("Notification handler setup complete")

                    while (
                        self.config.use_encryption
                        and not self.encryption.is_ready_for_commands
                    ):
                        await asyncio.sleep(5)
                        self.logger.debug("Encryption handshake not finished yet")

                    for register in registers:
                        body = register.parse_response(
                            await self._async_send_command(register)
                        )

                        self.logger.debug("Raw data: %s", body)

                        if raw:
                            d = {}
                            d[str(register.starting_address)] = body
                            parsed_data.update(d)
                            continue

                        parsed = self.bluetti_device.parse(
                            register.starting_address, body
                        )

                        self.logger.debug("Parsed data: %s", parsed)

                        parsed_data.update(parsed)

                    for pack in range(1, self.bluetti_device.max_packs + 1):
                        body = register.parse_response(
                            await self._async_send_command(
                                self.bluetti_device.get_pack_selector(pack),
                            )
                        )

                        # We need to wait for the powerstation to populate all registers
                        await asyncio.sleep(3)

                        for register in pack_registers:
                            body = register.parse_response(
                                await self._async_send_command(register)
                            )

                            self.logger.debug("Raw data: %s", body)

                            if raw:
                                d = {}
                                d[str(register.starting_address)] = body
                                parsed_data.update(d)
                                continue

                            parsed = self.bluetti_device.parse(
                                register.starting_address,
                                body,
                                pack_num=pack,
                            )

                            self.logger.debug("Parsed data: %s", parsed)

                            parsed_data.update(parsed)

            except TimeoutError:
                self.logger.debug("Timeout")
                return None
            except BleakError as err:
                self.logger.debug("Bleak error: %s", err)
                return None
            except BaseException as err:
                self.logger.debug("Unknown error %s", err)
                return None
            finally:
                if self.client:
                    if self.has_notifier:
                        try:
                            await self.client.stop_notify(NOTIFY_UUID)
                            self.logger.debug("Stopped notifier")
                        except:
                            # Ignore errors here
                            pass
                        self.has_notifier = False

                    await self.client.disconnect()
                    self.logger.debug("Disconnected from device")

            self.client = None
            self.device = None

            # Reset Encryption keys
            self.encryption.reset()
            self.encrypted_buffer.clear()

            # Check if dict is empty
            if len(parsed_data.keys()) == 0:
                return None

            return parsed_data

    async def _async_send_command(self, registers: DeviceRegister) -> bytes:
        """Send command and return response"""
        self.current_registers = registers
        self.notify_response = bytearray()
        self.notify_future = self.create_future()
        self.encrypted_buffer.clear()

        command_bytes = bytes(registers)

        # Encrypt command
        if self.config.use_encryption is True:
            if not self.encryption.is_ready_for_commands:
                return bytes()
            command_bytes = self.encryption.aes_encrypt(
                command_bytes, self.encryption.secure_aes_key, None
            )

        if not self.client:
            return bytes()

        try:
            # Make request
            await self.client.write_gatt_char(WRITE_UUID, command_bytes)

            self.logger.debug("Request sent (%s)", registers)

            # Wait for response
            res = await asyncio.wait_for(self.notify_future, timeout=5)

            self.logger.debug("Got response")

            return cast(bytes, res)
        except:
            self.logger.debug("Error while reading data")

        return bytes()

    def _calculate_expected_encrypted_length(self, buffer: bytearray) -> int | None:
        """Calculate expected total length of an encrypted message."""
        if len(buffer) < 2:
            return None

        data_len = (buffer[0] << 8) + buffer[1]

        key, iv = self.encryption.getKeyIv()
        if iv is None:
            header_size = 6
        else:
            header_size = 2

        padded_len = (
            (data_len + AES_BLOCK_SIZE - 1) // AES_BLOCK_SIZE
        ) * AES_BLOCK_SIZE

        return header_size + padded_len

    async def _notification_handler(
        self, _: BleakGATTCharacteristic, data: bytes | bytearray
    ) -> None:
        """Handle bt data."""
        self.logger.debug("Got new data (%d bytes)", len(data))

        if not self.client:
            return

        if self.config.use_encryption is True:
            message = Message(data)

            if message.is_pre_key_exchange:
                message.verify_checksum()

                if message.type == MessageType.CHALLENGE:
                    challenge_response = self.encryption.msg_challenge(message)

                    if not challenge_response:
                        return

                    await self.client.write_gatt_char(WRITE_UUID, challenge_response)
                    return

                if message.type == MessageType.CHALLENGE_ACCEPTED:
                    self.logger.debug("Challenge accepted")
                    return

                return

            if self.encryption.unsecure_aes_key is None:
                self.logger.debug(
                    "Received encrypted message before key initialization"
                )
                return

            self.encrypted_buffer.extend(data)

            expected_len = self._calculate_expected_encrypted_length(
                self.encrypted_buffer
            )

            if expected_len is None:
                return

            if len(self.encrypted_buffer) < expected_len:
                self.logger.debug(
                    "Buffering fragment: %d/%d bytes",
                    len(self.encrypted_buffer),
                    expected_len,
                )
                return

            complete_message = bytes(self.encrypted_buffer[:expected_len])

            if len(self.encrypted_buffer) > expected_len:
                self.encrypted_buffer = self.encrypted_buffer[expected_len:]
            else:
                self.encrypted_buffer.clear()

            key, iv = self.encryption.getKeyIv()

            try:
                decrypted = Message(
                    self.encryption.aes_decrypt(complete_message, key, iv)
                )
            except ValueError as e:
                self.logger.debug("Decryption failed: %s", e)
                self.encrypted_buffer.clear()
                return

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

        if self.notify_future is None:
            return

        self.notify_future.set_result(self.notify_response)
