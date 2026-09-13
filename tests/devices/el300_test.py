import asyncio
import unittest

from bluetti_bt_lib import DeviceReader, FieldName
from bluetti_bt_lib.devices import EL300
from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption


class TestEL300(unittest.IsolatedAsyncioTestCase):
    async def test_core_fields(self):
        ble_mock = ClientMockNoEncryption()
        ble_mock.add_r_int(102, 83)
        ble_mock.add_r_sstr(110, "EL300", 6)
        ble_mock.add_r_sn(116, 2551110023321)
        ble_mock.add_r_int(140, 12)
        ble_mock.add_r_int(142, 293)
        ble_mock.add_r_int(144, 0)
        ble_mock.add_r_int(146, 1052)

        reader = DeviceReader(
            "00:11:00:11:00:11",
            EL300(),
            asyncio.Future,
            ble_client=ble_mock,
        )

        data = await reader.read()

        self.assertIsNotNone(data)
        self.assertEqual(data.get(FieldName.DEVICE_TYPE.value), "EL300")
        self.assertEqual(data.get(FieldName.DEVICE_SN.value), 2551110023321)
        self.assertEqual(data.get(FieldName.BATTERY_SOC.value), 83)
        self.assertEqual(data.get(FieldName.DC_OUTPUT_POWER.value), 12)
        self.assertEqual(data.get(FieldName.AC_OUTPUT_POWER.value), 293)
        self.assertEqual(data.get(FieldName.DC_INPUT_POWER.value), 0)
        self.assertEqual(data.get(FieldName.AC_INPUT_POWER.value), 1052)
