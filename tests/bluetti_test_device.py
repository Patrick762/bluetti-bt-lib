"""
Mock Bluetti device for testing Bluetooth interactions.

This module provides BluettiTestDevice, an async context manager that mocks
Bluetti device Bluetooth interactions by intercepting bleak BLE calls and
simulating MODBUS protocol responses.
"""

from __future__ import annotations

import asyncio
from collections import deque
from collections.abc import Buffer
from contextlib import ExitStack
from enum import Enum
import struct
from typing import Literal, Union, assert_never, cast
import uuid
from unittest.mock import patch, MagicMock

from bleak import BleakError
from bleak.backends.scanner import (
    BaseBleakScanner,
    AdvertisementData,
    AdvertisementDataCallback,
)
from bleak.backends.client import BaseBleakClient, NotifyCallback
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.descriptor import BleakGATTDescriptor
from bleak.backends.device import BLEDevice
from bleak.backends.service import BleakGATTService, BleakGATTServiceCollection

from bluetti_bt_lib.registers import modbus_crc


class RegisterMemory:
    """Manages device register state for mocking.

    Stores register values as 2-byte strings in a sparse dictionary.
    """

    def __init__(self) -> None:
        self._registers: dict[int, bytes] = {}

    def write_register(self, address: int, value: bytes) -> None:
        """Write a 2-byte value to a register.

        Args:
            address: Register address
            value: 2 bytes in big-endian format
        """
        if len(value) != 2:
            raise ValueError(f"Register value must be 2 bytes, got {len(value)}")
        self._registers[address] = value

    def write_registers(self, start_address: int, data: bytes) -> None:
        """Write multiple consecutive registers from byte data.

        Args:
            start_address: Starting register address
            data: Bytes to write (must be even length, 2 bytes per register)
        """
        if len(data) % 2 != 0:
            raise ValueError(f"Data must be even length, got {len(data)}")
        for i in range(0, len(data), 2):
            register_addr = start_address + (i // 2)
            self.write_register(register_addr, data[i : i + 2])

    def read_registers(self, start: int, count: int) -> bytes:
        """Read multiple consecutive registers.

        Args:
            start: Starting register address
            count: Number of registers to read

        Returns:
            Concatenated bytes for all registers (2 * count bytes total)
        """
        result = bytearray()
        for addr in range(start, start + count):
            # Return zeros for uninitialized registers
            result.extend(self._registers.get(addr, b"\x00\x00"))
        return bytes(result)


class MODBUSHandler:
    READ_HOLDING_REGISTERS = 3
    WRITE_SINGLE_REGISTER = 6
    WRITE_MULTIPLE_REGISTERS = 16

    ILLEGAL_FUNCTION = 1
    ILLEGAL_DATA_ADDRESS = 2
    ILLEGAL_DATA_VALUE = 3

    def __init__(
        self,
        register_memory: RegisterMemory,
        readable_ranges: list[range],
        writable_ranges: list[range],
    ) -> None:
        self._memory = register_memory
        self._readable_ranges = readable_ranges
        self._writable_ranges = writable_ranges

    def handle_command(self, cmd_bytes: bytes) -> bytes:
        if len(cmd_bytes) < 4:
            raise ValueError("Command too short")

        # Validate CRC
        if not self._validate_crc(cmd_bytes):
            raise ValueError("Invalid CRC in command")

        # Extract function code
        device_addr = cmd_bytes[0]
        function_code = cmd_bytes[1]

        # Route to appropriate handler
        if function_code == self.READ_HOLDING_REGISTERS:
            return self._handle_read_holding_registers(cmd_bytes)
        elif function_code == self.WRITE_SINGLE_REGISTER:
            return self._handle_write_single_register(cmd_bytes)
        elif function_code == self.WRITE_MULTIPLE_REGISTERS:
            return self._handle_write_multiple_registers(cmd_bytes)
        else:
            return self._generate_exception_response(
                device_addr, function_code, self.ILLEGAL_FUNCTION
            )

    def _handle_read_holding_registers(self, cmd_bytes: bytes) -> bytes:
        if len(cmd_bytes) != 8:
            raise ValueError("Command too short")

        device_addr, function_code, starting_addr, quantity = struct.unpack(
            "!BBHH", cmd_bytes[:6]
        )

        # Validate address range
        for addr in range(starting_addr, starting_addr + quantity):
            if not self._is_readable(addr):
                return self._generate_exception_response(
                    device_addr, function_code, self.ILLEGAL_DATA_ADDRESS
                )

        # Build response
        data = self._memory.read_registers(starting_addr, quantity)
        response = struct.pack("!BBB", device_addr, function_code, 2 * quantity)
        return self._add_crc(response + data)

    def _handle_write_single_register(self, cmd_bytes: bytes) -> bytes:
        if len(cmd_bytes) != 8:
            raise ValueError("Command too short")

        device_addr, function_code, address, value = struct.unpack(
            "!BBH2s", cmd_bytes[:6]
        )

        # Validate address
        if not self._is_writable(address):
            return self._generate_exception_response(
                device_addr, function_code, self.ILLEGAL_DATA_ADDRESS
            )

        # Write register
        self._memory.write_register(address, value)

        # Echo back the command (standard MODBUS response for write)
        return cmd_bytes

    def _handle_write_multiple_registers(self, cmd_bytes: bytes) -> bytes:
        if len(cmd_bytes) < 11:
            raise ValueError("Command too short")

        device_addr, function_code, starting_addr, quantity, byte_count = struct.unpack(
            "!BBHHB", cmd_bytes[:7]
        )

        # Validate byte count
        if byte_count != quantity * 2:
            return self._generate_exception_response(
                device_addr, function_code, self.ILLEGAL_DATA_VALUE
            )

        # Validate command length - prefix + data + crc
        if len(cmd_bytes) != 7 + byte_count + 2:
            return self._generate_exception_response(
                device_addr, function_code, self.ILLEGAL_DATA_VALUE
            )

        # Validate all addresses are writable
        for addr in range(starting_addr, starting_addr + quantity):
            if not self._is_writable(addr):
                return self._generate_exception_response(
                    device_addr, function_code, self.ILLEGAL_DATA_ADDRESS
                )

        # Write registers
        data = cmd_bytes[7 : 7 + byte_count]
        self._memory.write_registers(starting_addr, data)

        # Build response
        response = struct.pack(
            "!BBHH", device_addr, function_code, starting_addr, quantity
        )
        return self._add_crc(response)

    def _validate_crc(self, data: bytes) -> bool:
        calculated_crc = modbus_crc(data[:-2])
        expected_crc = struct.unpack("<H", data[-2:])[0]
        return calculated_crc == expected_crc

    def _add_crc(self, data: bytes) -> bytes:
        crc = modbus_crc(data)
        return data + struct.pack("<H", crc)

    def _generate_exception_response(
        self, device_addr: int, function_code: int, exception_code: int
    ) -> bytes:
        response = bytearray([device_addr, function_code + 0x80, exception_code])
        return self._add_crc(bytes(response))

    def _is_readable(self, address: int) -> bool:
        return any(address in r for r in self._readable_ranges)

    def _is_writable(self, address: int) -> bool:
        return any(address in r for r in self._writable_ranges)


class OverrideType(Enum):
    TIMEOUT = "timeout"
    CRC_ERROR = "crc_error"
    CONNECTION_ERROR = "connection_error"
    RESPONSE_OVERRIDE = "response_override"


class ConnectionErrorType(Enum):
    BLEAK = "bleak"
    EOF = "eof"


# FailureInjector overrides
Override = Union[
    tuple[Literal[OverrideType.TIMEOUT]],
    tuple[Literal[OverrideType.CRC_ERROR]],
    tuple[Literal[OverrideType.CONNECTION_ERROR], ConnectionErrorType],
    tuple[Literal[OverrideType.RESPONSE_OVERRIDE], bytes],
]


class FailureInjector:
    """Manages failure and response injection for testing.

    Maintains a FIFO queue of overrides that are consumed in the exact order
    they were injected. Each check method only consumes an override from the
    queue if the front item matches its expected type.
    """

    def __init__(self) -> None:
        self._override_queue: deque[Override] = deque()

    def inject_timeout(self, count: int = 1):
        for _ in range(count):
            self._override_queue.append((OverrideType.TIMEOUT,))

    def inject_crc_error(self, count: int = 1):
        for _ in range(count):
            self._override_queue.append((OverrideType.CRC_ERROR,))

    def inject_connection_error(
        self,
        error_type: ConnectionErrorType = ConnectionErrorType.BLEAK,
        count: int = 1,
    ):
        for _ in range(count):
            self._override_queue.append((OverrideType.CONNECTION_ERROR, error_type))

    def override_next_response(self, response_bytes: bytes):
        self._override_queue.append((OverrideType.RESPONSE_OVERRIDE, response_bytes))

    def should_timeout(self) -> bool:
        if self._override_queue and self._override_queue[0][0] == OverrideType.TIMEOUT:
            self._override_queue.popleft()
            return True
        return False

    def should_corrupt_crc(self) -> bool:
        if (
            self._override_queue
            and self._override_queue[0][0] == OverrideType.CRC_ERROR
        ):
            self._override_queue.popleft()
            return True
        return False

    def should_fail_connection(self) -> Exception | None:
        """Check if next override in queue is a connection error, consuming it if so.

        Returns:
            Exception to raise, or None if no connection error queued
        """
        if (
            self._override_queue
            and self._override_queue[0][0] == OverrideType.CONNECTION_ERROR
        ):
            override = self._override_queue.popleft()
            assert override[0] is OverrideType.CONNECTION_ERROR
            if override[1] == ConnectionErrorType.BLEAK:
                return BleakError("Injected BleakError")
            elif override[1] == ConnectionErrorType.EOF:
                return EOFError("Injected EOFError")
            assert_never(override[1])
        return None

    def get_response_override(self) -> bytes | None:
        """Check if next override in queue is a response override, consuming it if so.

        Returns:
            Custom response bytes, or None if no response override queued
        """
        if (
            self._override_queue
            and self._override_queue[0][0] == OverrideType.RESPONSE_OVERRIDE
        ):
            override = self._override_queue.popleft()
            assert override[0] is OverrideType.RESPONSE_OVERRIDE
            return override[1]
        return None


class BluettiBleakScanner(BaseBleakScanner):
    def __init__(
        self,
        device: BLEDevice,
        detection_callback: AdvertisementDataCallback | None = None,
        service_uuids: list[str] | None = None,
    ) -> None:
        super().__init__(detection_callback, service_uuids)
        self._device = device

    async def start(self) -> None:
        # In the current version of Bleak we have to add devices after start
        # returns, so queue up advertisement
        asyncio.create_task(self._advertise_device())

    async def _advertise_device(self) -> None:
        name = cast(str, self._device.name)
        advertisement_data = AdvertisementData(
            local_name=name,
            manufacturer_data={},
            service_data={},
            service_uuids=[BluettiBleakClient.SERVICE_UUID],
            tx_power=0,
            rssi=-60,
            platform_data=(None,),
        )
        device = self.create_or_update_device(
            "bluetti", self._device.address, name, {}, advertisement_data
        )
        self.call_detection_callbacks(device, advertisement_data)

    async def stop(self) -> None:
        pass

    def set_scanning_filter(self, **kwargs) -> None:
        pass


class BluettiBleakClient(BaseBleakClient):
    SERVICE_UUID = "FF00"
    WRITE_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"
    NOTIFY_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"

    def __init__(
        self,
        device: BLEDevice,
        modbus_handler: MODBUSHandler,
        failure_injector: FailureInjector,
    ):
        super().__init__(device)
        self._modbus_handler = modbus_handler
        self._failure_injector = failure_injector
        self._connected: bool = False
        self._notification_callbacks: dict[str, NotifyCallback] = {}

    @property
    def mtu_size(self) -> int:
        return 23

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def connect(self, pair: bool, **kwargs) -> None:
        exc = self._failure_injector.should_fail_connection()
        if exc:
            raise exc
        self._connected = True
        await self.get_services()

    async def disconnect(self) -> None:
        self._connected = False
        pass

    async def get_services(self, **kwargs) -> BleakGATTServiceCollection:
        if self.services is not None:
            return self.services

        services = BleakGATTServiceCollection()
        service = BleakGATTService(None, 1, self.SERVICE_UUID)
        services.add_service(service)
        services.add_characteristic(
            BleakGATTCharacteristic(
                None,
                1,
                self.WRITE_UUID,
                ["write", "write-without-response"],
                lambda: 20,
                service,
            )
        )
        services.add_characteristic(
            BleakGATTCharacteristic(
                None, 2, self.NOTIFY_UUID, ["notify"], lambda: 20, service
            )
        )
        self.services = services

        return self.services

    async def start_notify(
        self,
        characteristic: BleakGATTCharacteristic,
        callback: NotifyCallback,
        **kwargs,
    ) -> None:
        self._notification_callbacks[characteristic.uuid] = callback

    async def stop_notify(
        self, char_specifier: Union[BleakGATTCharacteristic, int, str, uuid.UUID]
    ) -> None:
        if not isinstance(char_specifier, BleakGATTCharacteristic):
            services = await self.get_services()
            characteristic = services.get_characteristic(char_specifier)
        else:
            characteristic = char_specifier
        if not characteristic:
            raise ValueError("invalid char specifier")
        del self._notification_callbacks[characteristic.uuid]

    async def write_gatt_char(
        self,
        characteristic: BleakGATTCharacteristic,
        data: Buffer,
        response: bool,
    ) -> None:
        # Only handle writes to the write characteristic
        if characteristic.uuid != self.WRITE_UUID:
            raise ValueError("Invalid write characteristic uuid")

        # Check for connection error
        exc = self._failure_injector.should_fail_connection()
        if exc:
            raise exc

        # Check for timeout - do nothing in that case
        if self._failure_injector.should_timeout():
            return

        # Process MODBUS command
        override_response = self._failure_injector.get_response_override()
        if override_response is not None:
            response_bytes = override_response
        else:
            response_bytes = self._modbus_handler.handle_command(bytes(data))
        response_data = bytearray(response_bytes)

        # Check for CRC corruption
        if self._failure_injector.should_corrupt_crc():
            response_data[-1] ^= 0xFF

        # Invoke notification callback with response
        callback = self._notification_callbacks.get(self.NOTIFY_UUID)
        if callback:
            chunk_size = self.mtu_size - 3
            for i in range(0, len(response_data), chunk_size):
                chunk = response_data[i : i + chunk_size]
                callback(chunk)

    async def pair(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    async def unpair(self) -> None:
        raise NotImplementedError()

    async def read_gatt_char(
        self,
        characteristic: BleakGATTCharacteristic,
        **kwargs,
    ) -> bytearray:
        raise NotImplementedError()

    async def read_gatt_descriptor(
        self, descriptor: BleakGATTDescriptor, **kwargs
    ) -> bytearray:
        raise NotImplementedError()

    async def write_gatt_descriptor(
        self, descriptor: BleakGATTDescriptor, data: Buffer
    ) -> None:
        raise NotImplementedError()


class BluettiTestDevice:
    """Async context manager for mocking Bluetti device Bluetooth interactions.

    Usage:
        async with BluettiTestDevice(
            name='AC300123456789',
            register_data: [(10, b'datahere'), (70, b'moredata')],
            readable_ranges: [range(1, 50), range(3000, 3062)],
            writable_ranges: [range(3000, 3062)],
        ) as mock:
            client = BluetoothClient(mock.ble_device)
            await client.run()

    The context manager automatically patches bleak to intercept Bluetooth
    calls and simulate MODBUS responses.
    """

    def __init__(
        self,
        name: str,
        register_data: list[tuple[int, bytes]],
        readable_ranges: list[range],
        writable_ranges: list[range],
    ):
        """Initialize the test device.

        Args:
            name: Device bluetooth name
            register_data: list of (start address, bytes) tuples to fill memory
            readable_ranges: list of readable register ranges
            writable_ranges: list of writable register ranges
        """
        self._ble_device = MagicMock()
        self._ble_device.name = name
        self._ble_device.address = "testdevice"

        self._register_memory = RegisterMemory()
        for start_address, data in register_data:
            self._register_memory.write_registers(start_address, data)

        self._modbus_handler = MODBUSHandler(
            self._register_memory, readable_ranges, writable_ranges
        )

        self._failure_injector = FailureInjector()

        self._exit_stack: ExitStack | None = None
        self._client: BluettiBleakClient | None = None

    @property
    def ble_device(self) -> BLEDevice:
        """Mock BleakDevice to initialize BleakClient with."""
        return self._ble_device

    @property
    def register_memory(self) -> RegisterMemory:
        """Access to register memory for reading or writing to device directly."""
        return self._register_memory

    def inject_timeout(self, count: int = 1):
        """Queue timeout failures for the next N commands."""
        self._failure_injector.inject_timeout(count)

    def inject_crc_error(self, count: int = 1):
        """Queue CRC errors for the next N commands."""
        self._failure_injector.inject_crc_error(count)

    def inject_connection_error(
        self,
        error_type: ConnectionErrorType = ConnectionErrorType.BLEAK,
        count: int = 1,
    ):
        """Queue connection errors for the next N commands.

        Args:
            error_type: Type of error to inject
            count: Number of commands to fail
        """
        self._failure_injector.inject_connection_error(error_type, count)

    def override_next_response(self, response_bytes: bytes):
        """Override the next command response with custom bytes."""
        self._failure_injector.override_next_response(response_bytes)

    async def disconnect(self):
        assert self._client is not None
        await self._client.disconnect()

    def __enter__(self):
        self._exit_stack = ExitStack()

        # Patch BleakScanner
        def mock_scanner_factory(
            detection_callback: AdvertisementDataCallback | None = None,
            service_uuids: list[str] | None = None,
            scanning_mode: Literal["active", "passive"] = "active",
            **kwargs,
        ):
            return BluettiBleakScanner(
                self._ble_device, detection_callback, service_uuids
            )

        self._exit_stack.enter_context(
            patch(
                "bleak.get_platform_scanner_backend_type",
                return_value=(mock_scanner_factory, "bluetti"),
            )
        )

        # Patch BleakClient
        self._client = BluettiBleakClient(
            self._ble_device, self._modbus_handler, self._failure_injector
        )

        def mock_client_factory(address_or_ble_device: Union[BLEDevice, str], **kwargs):
            if isinstance(address_or_ble_device, BLEDevice):
                address = address_or_ble_device.address
            else:
                address = address_or_ble_device

            if address != self._ble_device.address:
                raise ValueError(
                    f"Unexpected address for mocked BleakClient: {address}"
                )

            return self._client

        self._exit_stack.enter_context(
            patch(
                "bleak.get_platform_client_backend_type",
                return_value=(mock_client_factory, "bluetti"),
            )
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self._exit_stack is not None
        self._exit_stack.__exit__(exc_type, exc_val, exc_tb)
