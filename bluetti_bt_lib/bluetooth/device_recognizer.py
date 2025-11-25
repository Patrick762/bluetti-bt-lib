import asyncio
import logging
from typing import Any, Callable, List
from bleak import BleakClient

from ..fields import FieldName
from ..base_devices import BluettiDevice, BaseDeviceV1, BaseDeviceV2
from ..bluetooth import DeviceReader, DeviceReaderConfig

_LOGGER = logging.getLogger(__name__)


class DeviceRecognizerResult:
    def __init__(
        self, name: str, iot_version: int, encrypted: bool, sn: str | None = None
    ):
        self.name = name
        self.iot_version = iot_version
        self.encrypted = encrypted
        self.sn = sn
        self.full_name = name + sn


async def recognize_device(
    bleak_client: BleakClient,
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
                bleak_client,
                bluetti_device,
                future_builder_method,
                DeviceReaderConfig(
                    timeout=8,
                    use_encryption=True,
                ),
            ),
            DeviceReader(
                bleak_client,
                bluetti_device,
                future_builder_method,
                DeviceReaderConfig(timeout=3),
            ),
        ]

        for device_reader in device_readers:

            # We only need 6 registers to get the device type
            data = await device_reader.read(
                bluetti_device.get_device_type_registers(),
            )

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

            data = await device_reader.read(
                bluetti_device.get_device_sn_registers(),
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

            if isinstance(sn_data, str) or sn_data == "":
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
