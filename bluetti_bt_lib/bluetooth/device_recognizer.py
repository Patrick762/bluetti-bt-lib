import asyncio
import logging
from typing import Any, Callable, List

from ..base_devices import BluettiDevice, BaseDeviceV1, BaseDeviceV2
from ..bluetooth import DeviceReader, DeviceReaderConfig
from ..devices import DEVICE_NAME_RE
from ..fields import FieldName
from .exceptions import (
    DeviceNotFoundError,
    ConnectionFailedError,
    EncryptionHandshakeError,
)

_LOGGER = logging.getLogger(__name__)


class DeviceRecognizerResult:
    def __init__(
        self, name: str, iot_version: int, encrypted: bool, sn: int | None = None
    ):
        self.name = name
        self.iot_version = iot_version
        self.encrypted = encrypted
        self.sn = sn
        self.full_name = name + str(sn)


async def recognize_device(
    mac: str,
    future_builder_method: Callable[[], asyncio.Future[Any]],
) -> DeviceRecognizerResult | None:
    # Since we don't know the type we use the base device
    bluetti_devices: List[BluettiDevice] = [
        BaseDeviceV2(),
        BaseDeviceV1(),
    ]

    for bluetti_device in bluetti_devices:
        # Create device builder
        device_readers = [
            DeviceReader(
                mac,
                bluetti_device,
                future_builder_method,
                DeviceReaderConfig(
                    timeout=15,
                    use_encryption=True,
                ),
            ),
            DeviceReader(
                mac,
                bluetti_device,
                future_builder_method,
                DeviceReaderConfig(timeout=8),
            ),
        ]

        for device_reader in device_readers:

            # We only need 6 registers to get the device type
            try:
                data = await device_reader.read(
                    bluetti_device.get_device_type_registers(),
                )
            except DeviceNotFoundError:
                # Device not in range — no point trying other protocols
                raise
            except (ConnectionFailedError, EncryptionHandshakeError):
                # Try next protocol variant
                continue

            if data is None:
                continue

            type_data = data.get(FieldName.DEVICE_TYPE.value)

            if type_data is None:
                # We have a problem
                _LOGGER.error("No data in device type type_data")
                continue

            if not isinstance(type_data, str):
                # We have a problem
                _LOGGER.error("Invalid data in device type type_data")
                continue

            if type_data == "":
                # Empty string is not a valid device type
                continue

            if DEVICE_NAME_RE.match(type_data + "12345678") is None:
                # Some V2 Devices populate the V1 register for type, so we need to check here
                _LOGGER.warning("Device has populated type_data with trash data")
                continue

            try:
                data = await device_reader.read(
                    bluetti_device.get_device_sn_registers(),
                )
            except (DeviceNotFoundError, ConnectionFailedError, EncryptionHandshakeError):
                return DeviceRecognizerResult(
                    type_data,
                    bluetti_device.get_iot_version(),
                    device_reader.config.use_encryption,
                    "000000000000",  # Use dummy SN
                )

            if data is None:
                # Should never happen
                return DeviceRecognizerResult(
                    type_data,
                    bluetti_device.get_iot_version(),
                    device_reader.config.use_encryption,
                    "000000000000",  # Use dummy SN
                )

            sn_data = data.get(FieldName.DEVICE_SN.value)

            if not isinstance(sn_data, int) or sn_data == "":
                # Should never happen
                return DeviceRecognizerResult(
                    type_data,
                    bluetti_device.get_iot_version(),
                    device_reader.config.use_encryption,
                    "000000000000",  # Use dummy SN
                )

            return DeviceRecognizerResult(
                type_data,
                bluetti_device.get_iot_version(),
                device_reader.config.use_encryption,
                sn_data,
            )

    return None
