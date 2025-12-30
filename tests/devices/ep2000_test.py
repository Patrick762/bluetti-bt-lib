import asyncio
from decimal import Decimal
import unittest

from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption
from bluetti_bt_lib.devices import EP600
from bluetti_bt_lib import DeviceReader, FieldName


class TestEP2000(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._createMock()

    def _createMock(self):
        self.ble_mock = ClientMockNoEncryption()

        self.ble_mock.add_r_int(102, 70)
        self.ble_mock.add_r_sstr(110, "EP2000", 6)
        self.ble_mock.add_r_sn(116, 2000000000000)

    async def test_ep2000(self):
        device = EP600()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertIsNotNone(data)

        self.assertEqual(data.get(FieldName.BATTERY_SOC.value), 70)
        self.assertEqual(data.get(FieldName.DEVICE_TYPE.value), "EP2000")
        self.assertEqual(data.get(FieldName.DEVICE_SN.value), 2000000000000)
