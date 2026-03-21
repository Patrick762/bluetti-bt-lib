import asyncio
import logging
from typing import Callable

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from ..const import NOTIFY_UUID, WRITE_UUID
from ..utils.privacy import mac_loggable
from .encryption import BluettiEncryption, Message, MessageType


class DeviceConnection:
    """Manages a persistent BLE connection shared between DeviceReader and DeviceWriter.

    Owns the BleakClient and BluettiEncryption session. Handles the ECDH handshake
    once on connect, then routes incoming notifications:
    - Handshake messages are handled internally.
    - Modbus data responses are dispatched to the data_callback set by DeviceReader.
    """

    def __init__(self, address: str, use_encryption: bool = False) -> None:
        self._address = address
        self._use_encryption = use_encryption
        self._client: BleakClientWithServiceCache | None = None
        self._encryption = BluettiEncryption()
        self._handshake_complete: asyncio.Event | None = None
        self._data_callback: Callable[[bytes], None] | None = None
        self.logger = logging.getLogger(
            f"{__name__}.{mac_loggable(address).replace(':', '_')}"
        )

    @property
    def address(self) -> str:
        return self._address

    @property
    def client(self) -> BleakClientWithServiceCache | None:
        return self._client

    @property
    def encryption(self) -> BluettiEncryption:
        return self._encryption

    @property
    def is_connected(self) -> bool:
        return self._client is not None and self._client.is_connected

    def set_data_callback(self, callback: Callable[[bytes], None]) -> None:
        """Called by DeviceReader before sending a command to receive the response."""
        self._data_callback = callback

    def clear_data_callback(self) -> None:
        """Called by DeviceReader after receiving the response."""
        self._data_callback = None

    async def connect(self) -> bool:
        """Scan for device, establish connection, run ECDH handshake if needed."""
        self._encryption.reset()
        try:
            device = await self._find_device()
            if device is None:
                return False
            self._client = await self._establish_client(device)
            await self._subscribe_notifications()
            if self._use_encryption:
                await self._wait_for_handshake()
            self.logger.debug("Connected successfully")
            return True
        except (BleakError, TimeoutError, asyncio.TimeoutError) as err:
            self.logger.warning("Connection failed: %s", err)
            return False

    async def ensure_connected(self) -> bool:
        """Reconnect if the connection was dropped."""
        if self.is_connected:
            return True
        self.logger.debug("Connection lost, reconnecting")
        return await self.connect()

    async def disconnect(self) -> None:
        """Explicitly close the connection and reset encryption state."""
        await self._stop_notifications()
        await self._disconnect_client()
        self._encryption.reset()
        self._client = None

    async def _find_device(self) -> BLEDevice | None:
        """Scan BLE for the device by address."""
        self.logger.debug("Scanning for device %s", mac_loggable(self._address))
        device = await BleakScanner.find_device_by_address(self._address, timeout=5)
        if device is None:
            self.logger.error("Device not found: %s", mac_loggable(self._address))
        return device

    async def _establish_client(self, device: BLEDevice) -> BleakClientWithServiceCache:
        """Create and connect a BleakClient using bleak_retry_connector."""
        self.logger.debug("Establishing connection")
        return await establish_connection(
            BleakClientWithServiceCache,
            device,
            device.name or "Unknown Device",
            max_attempts=10,
        )

    async def _subscribe_notifications(self) -> None:
        """Register the single notification handler on NOTIFY_UUID."""
        await self._client.start_notify(NOTIFY_UUID, self._on_notification)
        self.logger.debug("Notification handler registered")

    async def _wait_for_handshake(self) -> None:
        """Wait until the ECDH key exchange is complete."""
        self._handshake_complete = asyncio.Event()
        self.logger.debug("Waiting for encryption handshake")
        try:
            await asyncio.wait_for(self._handshake_complete.wait(), timeout=12)
        except asyncio.TimeoutError:
            raise TimeoutError("Encryption handshake timed out")
        self.logger.debug("Encryption handshake complete")

    async def _on_notification(self, _sender: int, data: bytearray) -> None:
        """Route each incoming BLE notification to the right handler."""
        message = Message(data)
        if message.is_pre_key_exchange:
            await self._handle_pre_key_message(message)
        elif self._use_encryption:
            await self._handle_encrypted_message(message)
        else:
            self._dispatch_data(bytes(data))

    async def _handle_pre_key_message(self, message: Message) -> None:
        """Handle unencrypted handshake: CHALLENGE and CHALLENGE_ACCEPTED."""
        message.verify_checksum()
        if message.type == MessageType.CHALLENGE:
            self.logger.debug("Received challenge, sending response")
            response = self._encryption.msg_challenge(message)
            await self._client.write_gatt_char(WRITE_UUID, response)
        elif message.type == MessageType.CHALLENGE_ACCEPTED:
            self.logger.debug("Challenge accepted, starting key exchange")

    async def _handle_encrypted_message(self, message: Message) -> None:
        """Decrypt the message, then route to key exchange or data handler."""
        if self._encryption.unsecure_aes_key is None:
            self.logger.warning("Received encrypted message before challenge completed")
            return
        key, iv = self._encryption.getKeyIv()
        decrypted = Message(self._encryption.aes_decrypt(message.buffer, key, iv))
        if decrypted.is_pre_key_exchange:
            await self._handle_encrypted_key_message(decrypted)
        else:
            self._dispatch_data(bytes(decrypted.buffer))

    async def _handle_encrypted_key_message(self, decrypted: Message) -> None:
        """Handle the encrypted part of ECDH: PEER_PUBKEY and PUBKEY_ACCEPTED."""
        decrypted.verify_checksum()
        if decrypted.type == MessageType.PEER_PUBKEY:
            self.logger.debug("Received peer public key, sending ours")
            response = self._encryption.msg_peer_pubkey(decrypted)
            await self._client.write_gatt_char(WRITE_UUID, response)
        elif decrypted.type == MessageType.PUBKEY_ACCEPTED:
            self.logger.debug("Key exchange complete, shared secret established")
            self._encryption.msg_key_accepted(decrypted)
            if self._handshake_complete is not None:
                self._handshake_complete.set()

    def _dispatch_data(self, data: bytes) -> None:
        """Deliver a Modbus response to the active data callback."""
        if self._data_callback is not None:
            self._data_callback(data)
        else:
            self.logger.debug("Received data but no callback is registered")

    async def _stop_notifications(self) -> None:
        if self._client is not None:
            try:
                await self._client.stop_notify(NOTIFY_UUID)
            except Exception:
                pass

    async def _disconnect_client(self) -> None:
        if self._client is not None:
            try:
                await self._client.disconnect()
            except Exception:
                pass
