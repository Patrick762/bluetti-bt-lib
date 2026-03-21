import asyncio
import logging
import async_timeout
from typing import Any, Callable, List, cast
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from .device_connection import DeviceConnection
from .encryption import BluettiEncryption, Message, MessageType
from ..base_devices import BluettiDevice
from ..const import NOTIFY_UUID, WRITE_UUID
from ..registers import ReadableRegisters, DeviceRegister
from ..utils.privacy import mac_loggable


class DeviceReaderConfig:
    def __init__(self, timeout: int = 60, use_encryption: bool = False, keep_alive_seconds: int = 0) -> None:
        self.timeout = timeout
        self.use_encryption = use_encryption
        self.keep_alive_seconds = keep_alive_seconds


class DeviceReader:
    def __init__(
        self,
        mac: str,
        bluetti_device: BluettiDevice,
        future_builder_method: Callable[[], asyncio.Future[Any]],
        config: DeviceReaderConfig = DeviceReaderConfig(),
        lock: asyncio.Lock = asyncio.Lock(),
        ble_client: BleakClient | None = None,
        connection: DeviceConnection | None = None,
    ) -> None:
        self.mac = mac
        self.bluetti_device = bluetti_device
        self.create_future = future_builder_method
        self.config = config
        self.polling_lock = lock
        self.connection = connection

        self.ble_client = ble_client
        """Used for unit tests"""

        self.logger = logging.getLogger(
            f"{__name__}.{mac_loggable(mac).replace(':', '_')}"
        )

        self.device = None
        self.client = None

        self.has_notifier = False
        self.current_registers = None
        self.notify_response = bytearray()
        self.notify_future: asyncio.Future[Any] | None = None
        self.encryption = BluettiEncryption()

    async def read(
        self, only_registers: List[ReadableRegisters] | None = None, raw: bool = False
    ) -> dict | None:

        registers = self.bluetti_device.get_polling_registers()
        pack_registers = self.bluetti_device.get_pack_polling_registers()

        if only_registers is not None:
            registers = only_registers
            pack_registers = []

        parsed_data: dict = {}

        self.logger.debug("Reading device registers")

        async with self.polling_lock:
            try:
                async with async_timeout.timeout(self.config.timeout):
                    if self.connection is not None:
                        await self._connect_via_shared_connection()
                    else:
                        await self._connect_standalone()

                    self.logger.debug("Notification handler setup complete")

                    for register in registers:
                        body = register.parse_response(
                            await self._async_send_command(register)
                        )

                        self.logger.debug("Raw data: %s", body)

                        if raw:
                            d = {}
                            d[register.starting_address] = body
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
                                d[register.starting_address] = body
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
                self.logger.warning("Timeout")
                return None
            except BleakError as err:
                self.logger.warning("Bleak error: %s", err)
                return None
            except Exception as err:
                self.logger.warning("Unknown error %s", err)
                return None
            finally:
                if self.connection is not None:
                    self.connection.clear_data_callback()
                    asyncio.ensure_future(self._deferred_disconnect())
                else:
                    await self._teardown_standalone_connection()

            if self.connection is None:
                self.encryption.reset()

            if not parsed_data:
                return None

            return parsed_data

    async def _connect_via_shared_connection(self) -> None:
        """Use an existing DeviceConnection instead of creating a new one."""
        connected = await self.connection.ensure_connected()
        if not connected:
            raise BleakError("Could not connect to device via shared connection")
        self.client = self.connection.client
        self.connection.set_data_callback(self._on_data)
        self.logger.debug("Using shared connection")

    async def _connect_standalone(self) -> None:
        """Scan, connect, and subscribe to notifications independently."""
        self.logger.debug("Searching for device")

        if self.ble_client:
            self.device = None
            self.client = self.ble_client
        else:
            self.device = await BleakScanner.find_device_by_address(
                self.mac, timeout=5
            )
            if self.device is None:
                self.logger.error("Device not found")
                raise BleakError("Device not found")
            self.logger.debug("Connecting to device")
            self.client = await establish_connection(
                BleakClientWithServiceCache,
                self.device,
                self.device.name or "Unknown Device",
                max_attempts=10,
            )

        self.logger.debug("Connected to device")

        if not self.has_notifier:
            await self.client.start_notify(NOTIFY_UUID, self._notification_handler)
            self.has_notifier = True

        while (
            self.config.use_encryption
            and not self.encryption.is_ready_for_commands
        ):
            await asyncio.sleep(5)
            self.logger.debug("Encryption handshake not finished yet")

    async def _deferred_disconnect(self) -> None:
        """Wait keep_alive_seconds, then disconnect to free the BLE slot."""
        if self.config.keep_alive_seconds > 0:
            await asyncio.sleep(self.config.keep_alive_seconds)
        await self.connection.disconnect()

    async def _teardown_standalone_connection(self) -> None:
        """Stop notifications and disconnect own client."""
        if self.has_notifier:
            try:
                await self.client.stop_notify(NOTIFY_UUID)
                self.logger.debug("Stopped notifier")
            except Exception:
                pass
            self.has_notifier = False
        if self.client:
            await self.client.disconnect()
            self.logger.debug("Disconnected from device")

    async def _async_send_command(self, registers: DeviceRegister) -> bytes:
        """Send a Modbus command and wait for the response."""
        self.current_registers = registers
        self.notify_response = bytearray()
        self.notify_future = self.create_future()

        command_bytes = self._build_command_bytes(registers)

        try:
            await self.client.write_gatt_char(WRITE_UUID, command_bytes)
            self.logger.debug("Request sent (%s)", registers)
            res = await asyncio.wait_for(self.notify_future, timeout=5)
            self.logger.debug("Got response")
            return cast(bytes, res)
        except Exception:
            self.logger.warning("Error while reading data")

        return bytes()

    def _build_command_bytes(self, registers: DeviceRegister) -> bytes:
        """Build and optionally encrypt the command bytes."""
        command_bytes = bytes(registers)
        if not self.config.use_encryption:
            return command_bytes
        enc = self.connection.encryption if self.connection is not None else self.encryption
        if not enc.is_ready_for_commands:
            return bytes()
        return enc.aes_encrypt(command_bytes, enc.secure_aes_key, None)

    def _on_data(self, data: bytes) -> None:
        """Receive a decrypted Modbus response from the shared DeviceConnection."""
        self.notify_response.extend(data)
        if self.notify_future is not None:
            self.notify_future.set_result(self.notify_response)

    async def _notification_handler(self, _: int, data: bytearray) -> None:
        """Handle BLE notifications in standalone (non-shared) mode."""
        self.logger.debug("Got new data")

        if self.config.use_encryption is True:
            message = Message(data)

            if message.is_pre_key_exchange:
                message.verify_checksum()

                if message.type == MessageType.CHALLENGE:
                    challenge_response = self.encryption.msg_challenge(message)
                    await self.client.write_gatt_char(WRITE_UUID, challenge_response)
                    return

                if message.type == MessageType.CHALLENGE_ACCEPTED:
                    self.logger.debug("Challenge accepted")
                    return

            if self.encryption.unsecure_aes_key is None:
                self.logger.error(
                    "Received encrypted message before key initialization"
                )

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

            # Handle as Modbus data response
            data = decrypted.buffer

        self._on_data(bytes(data))
