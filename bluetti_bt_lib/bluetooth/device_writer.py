import asyncio
import logging
from typing import Any
import async_timeout
from bleak import BleakClient
from bleak.exc import BleakError

from ..fields import FieldName
from ..const import WRITE_UUID
from ..base_devices import BluettiDevice

_LOGGER = logging.getLogger(__name__)


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

    async def write(self, field: str, value: Any):
        if self.config.use_encryption:
            _LOGGER.error("Encryption on writes is not yet supported")
            return

        available_fields = [f.name for f in self.bluetti_device.fields]
        if field not in available_fields:
            _LOGGER.error("Field not supported")
            return

        command = self.bluetti_device.build_write_command(field, value)

        _LOGGER.debug("Writing to device register")

        async with self.polling_lock:
            try:
                async with async_timeout.timeout(self.config.timeout):
                    if not self.client.is_connected:
                        _LOGGER.debug("Connecting to device")
                        await self.client.connect()

                    _LOGGER.debug("Connected to device")

                    await self.client.write_gatt_char(
                        WRITE_UUID,
                        bytes(command),
                    )

                    # Wait until device has changed value, otherwise reading register might reset it
                    await asyncio.sleep(5)

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
                await self.client.disconnect()
                _LOGGER.debug("Disconnected from device")
