import asyncio
import unittest

from bluetti_bt_lib.base_devices import BaseDeviceV1
from bluetti_bt_lib import DeviceReader
from bluetti_bt_lib.fields import FieldName
from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption


class TestDeviceReader(unittest.IsolatedAsyncioTestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.ble_mock = ClientMockNoEncryption()

        # Device type
        self.ble_mock.add_r_str(10, "AC300", 6)
        # Serial
        self.ble_mock.add_r_sn(17, 2300000000000)
        # DC input power
        self.ble_mock.add_r_int(36, 10)
        # AC input power
        self.ble_mock.add_r_int(37, 8)
        # AC output power
        self.ble_mock.add_r_int(38, 9)
        # AC output power
        self.ble_mock.add_r_int(39, 7)
        # SOC
        self.ble_mock.add_r_int(43, 78)

    async def test_read_all_correct(self):
        device = BaseDeviceV1()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertEqual(data.get(FieldName.D_INVERTER_TYPE.value), "AC300")
        self.assertEqual(data.get(FieldName.D_SERIAL.value), 2300000000000)
        self.assertEqual(data.get(FieldName.DC_I_P_TOTAL.value), 10)
        self.assertEqual(data.get(FieldName.AC_I_P_TOTAL.value), 8)
        self.assertEqual(data.get(FieldName.AC_O_P_TOTAL.value), 9)
        self.assertEqual(data.get(FieldName.DC_O_P_TOTAL.value), 7)
        self.assertEqual(data.get(FieldName.B_SOC_TOTAL.value), 78)

    async def test_read_soc_wrong(self):
        # SOC
        self.ble_mock.add_r_int(43, 1234)

        device = BaseDeviceV1()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertIsNone(data.get(FieldName.B_SOC_TOTAL.value))
