import asyncio
import unittest

from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption
from bluetti_bt_lib.base_devices import BaseDeviceV1
from bluetti_bt_lib import DeviceReader, FieldName


class TestV1(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._createMock()

    def _createMock(self):
        self.ble_mock = ClientMockNoEncryption()

        # Device type
        self.ble_mock.add_r_str(10, "AC300", 6)
        # Serial
        self.ble_mock.add_r_sn(17, 1000000000000)
        # SOC
        self.ble_mock.add_r_int(43, 1)
        # DC Input Power
        self.ble_mock.add_r_int(36, 500)
        # AC Input Power
        self.ble_mock.add_r_int(37, 600)
        # AC Output Power
        self.ble_mock.add_r_int(38, 2500)
        # DC Output Power
        self.ble_mock.add_r_int(39, 24)

    async def test_v1(self):
        device = BaseDeviceV1()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertEqual(data.get(FieldName.BATTERY_SOC.value), 1)
        self.assertEqual(data.get(FieldName.DEVICE_TYPE.value), "AC300")
        self.assertEqual(data.get(FieldName.DEVICE_SN.value), 1000000000000)
        self.assertEqual(data.get(FieldName.DC_INPUT_POWER.value), 500)
        self.assertEqual(data.get(FieldName.AC_INPUT_POWER.value), 600)
        self.assertEqual(data.get(FieldName.AC_OUTPUT_POWER.value), 2500)
        self.assertEqual(data.get(FieldName.DC_OUTPUT_POWER.value), 24)
