import asyncio
import unittest

from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption
from bluetti_bt_lib.base_devices import BaseDeviceV2
from bluetti_bt_lib import DeviceReader, FieldName


class TestV2(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._createMock()

    def _createMock(self):
        self.ble_mock = ClientMockNoEncryption()

        # Device type
        self.ble_mock.add_r_sstr(110, "AC70", 6)
        # Serial
        self.ble_mock.add_r_sn(116, 2000000000000)
        # SOC
        self.ble_mock.add_r_int(102, 2)

    async def test_v1(self):
        device = BaseDeviceV2()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertEqual(data.get(FieldName.BATTERY_SOC.value), 2)
        self.assertEqual(data.get(FieldName.DEVICE_TYPE.value), "AC70")
        self.assertEqual(data.get(FieldName.DEVICE_SN.value), 2000000000000)
