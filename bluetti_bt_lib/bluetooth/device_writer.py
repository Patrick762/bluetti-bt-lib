import asyncio
import logging
from typing import Any
from bleak import BleakClient
from bleak.exc import BleakError

from ..const import WRITE_UUID
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

        self.logger = logging.getLogger(
            f"{__name__}.{mac_loggable(bleak_client.address).replace(':', '_')}"
        )

    async def write(self, field: str, value: Any) -> None:
        if self.config.use_encryption:
            self.logger.debug("Encryption on writes is not yet supported")
            return

        available_fields = [f.name for f in self.bluetti_device.fields]
        if field not in available_fields:
            self.logger.debug("Field not supported")
            return

        command = self.bluetti_device.build_write_command(field, value)

        if command is None:
            self.logger.debug("Field is not writeable")
            return

        self.logger.debug("Writing to device register")

        async with self.polling_lock:
            try:
                async with asyncio.timeout(self.config.timeout):
                    if not self.client.is_connected:
                        self.logger.debug("Connecting to device")
                        await self.client.connect()

                    self.logger.debug("Connected to device")

                    self.logger.debug("Writing command: %s", command)

                    await self.client.write_gatt_char(
                        WRITE_UUID,
                        bytes(command),
                    )

                    self.logger.debug("Write successful")

            except TimeoutError:
                self.logger.debug("Timeout")
                return None
            except BleakError as err:
                self.logger.debug("Bleak error: %s", err)
                return None
            except BaseException as err:
                self.logger.debug("Unknown error: %s", err)
                return None
            finally:
                await self.client.disconnect()
                self.logger.debug("Disconnected from device")
