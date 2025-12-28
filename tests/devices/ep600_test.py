import asyncio
from decimal import Decimal
import unittest

from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption
from bluetti_bt_lib.devices import EP600
from bluetti_bt_lib import DeviceReader, FieldName


class TestEP600(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._createMock()

    def _createMock(self):
        self.ble_mock = ClientMockNoEncryption()

        # Power generation
        self.ble_mock.add_r_int(1202, 3505)

        # PV S1 Power
        self.ble_mock.add_r_int(1212, 1200)
        # PV S1 Voltage
        self.ble_mock.add_r_int(1213, 450)
        # PV S1 Current
        self.ble_mock.add_r_int(1214, 266)

        # PV S2 Power
        self.ble_mock.add_r_int(1220, 2300)
        # PV S2 Voltage
        self.ble_mock.add_r_int(1221, 480)
        # PV S2 Current
        self.ble_mock.add_r_int(1222, 479)

        # SM P1 Power
        self.ble_mock.add_r_int(1228, 0)
        # SM P1 Voltage
        self.ble_mock.add_r_int(1229, 0)
        # SM P1 Current
        self.ble_mock.add_r_int(1230, 0)

        # SM P2 Power
        self.ble_mock.add_r_int(1236, 0)
        # SM P2 Voltage
        self.ble_mock.add_r_int(1237, 0)
        # SM P2 Current
        self.ble_mock.add_r_int(1238, 0)

        # SM P3 Power
        self.ble_mock.add_r_int(1244, 0)
        # SM P3 Voltage
        self.ble_mock.add_r_int(1245, 0)
        # SM P3 Current
        self.ble_mock.add_r_int(1246, 0)

        # Grid Frequency
        self.ble_mock.add_r_int(1300, 500)

        # Grid P1 Power
        self.ble_mock.add_r_int(1313, 0)
        # Grid P1 Voltage
        self.ble_mock.add_r_int(1314, 0)
        # Grid P1 Current
        self.ble_mock.add_r_int(1315, 0)

        # Grid P2 Power
        self.ble_mock.add_r_int(1319, 0)
        # Grid P2 Voltage
        self.ble_mock.add_r_int(1320, 0)
        # Grid P2 Current
        self.ble_mock.add_r_int(1321, 0)

        # Grid P3 Power
        self.ble_mock.add_r_int(1325, 0)
        # Grid P3 Voltage
        self.ble_mock.add_r_int(1326, 0)
        # Grid P3 Current
        self.ble_mock.add_r_int(1327, 0)

        # AC Output Frequency
        self.ble_mock.add_r_int(1500, 500)

        # AC P1 Power
        self.ble_mock.add_r_int(1510, 5)
        # AC P1 Voltage
        self.ble_mock.add_r_int(1511, 0)
        # AC P1 Current
        self.ble_mock.add_r_int(1512, 0)

        # AC P2 Power
        self.ble_mock.add_r_int(1517, 77)
        # AC P2 Voltage
        self.ble_mock.add_r_int(1518, 0)
        # AC P2 Current
        self.ble_mock.add_r_int(1519, 0)

        # AC P3 Power
        self.ble_mock.add_r_int(1524, 9)
        # AC P3 Voltage
        self.ble_mock.add_r_int(1525, 0)
        # AC P3 Current
        self.ble_mock.add_r_int(1526, 0)

        # Control AC
        self.ble_mock.add_r_int(2011, 1)

        # Battery SOC Range Start
        self.ble_mock.add_r_int(2022, 20)
        # Battery SOC Range End
        self.ble_mock.add_r_int(2023, 80)

        # Control Generator
        self.ble_mock.add_r_int(2246, 0)

        # Grid Volt Min Val
        self.ble_mock.add_r_int(2435, 200)
        # Grid Volt Max Val
        self.ble_mock.add_r_int(2436, 245)

        # Grid Freq Min Val
        self.ble_mock.add_r_int(2437, 4800)
        # Grid Freq Max Val
        self.ble_mock.add_r_int(2438, 5200)

        # WiFi SSID
        self.ble_mock.add_r_sstr(12002, "MyHomeSSID", 16)

    async def test_ep600(self):
        device = EP600()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertIsNotNone(data)

        self.assertEqual(data.get(FieldName.POWER_GENERATION.value), Decimal('350.5'))

        self.assertEqual(data.get(FieldName.PV_S1_POWER.value), 1200)
        self.assertEqual(data.get(FieldName.PV_S1_VOLTAGE.value), Decimal('45.0'))
        self.assertEqual(data.get(FieldName.PV_S1_CURRENT.value), Decimal('26.6'))

        self.assertEqual(data.get(FieldName.PV_S2_POWER.value), 2300)
        self.assertEqual(data.get(FieldName.PV_S2_VOLTAGE.value), Decimal('48.0'))
        self.assertEqual(data.get(FieldName.PV_S2_CURRENT.value), Decimal('47.9'))

        self.assertEqual(data.get(FieldName.SM_P1_POWER.value), 0)
        self.assertEqual(data.get(FieldName.SM_P1_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.SM_P1_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.SM_P2_POWER.value), 0)
        self.assertEqual(data.get(FieldName.SM_P2_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.SM_P2_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.SM_P3_POWER.value), 0)
        self.assertEqual(data.get(FieldName.SM_P3_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.SM_P3_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.GRID_FREQUENCY.value), Decimal('50.0'))

        self.assertEqual(data.get(FieldName.GRID_P1_POWER.value), 0)
        self.assertEqual(data.get(FieldName.GRID_P1_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.GRID_P1_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.GRID_P2_POWER.value), 0)
        self.assertEqual(data.get(FieldName.GRID_P2_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.GRID_P2_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.GRID_P3_POWER.value), 0)
        self.assertEqual(data.get(FieldName.GRID_P3_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.GRID_P3_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.AC_OUTPUT_FREQUENCY.value), Decimal('50.0'))
        
        self.assertEqual(data.get(FieldName.AC_P1_POWER.value), 5)
        self.assertEqual(data.get(FieldName.AC_P1_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.AC_P1_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.AC_P2_POWER.value), 77)
        self.assertEqual(data.get(FieldName.AC_P2_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.AC_P2_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.AC_P3_POWER.value), 9)
        self.assertEqual(data.get(FieldName.AC_P3_VOLTAGE.value), 0)
        self.assertEqual(data.get(FieldName.AC_P3_CURRENT.value), 0)

        self.assertEqual(data.get(FieldName.CTRL_AC.value), True)

        self.assertEqual(data.get(FieldName.BATTERY_SOC_RANGE_START.value), 20)
        self.assertEqual(data.get(FieldName.BATTERY_SOC_RANGE_END.value), 80)

        self.assertEqual(data.get(FieldName.CTRL_GENERATOR.value), False)

        self.assertEqual(data.get(FieldName.GRID_VOLT_MIN_VAL.value), Decimal('20.0'))
        self.assertEqual(data.get(FieldName.GRID_VOLT_MAX_VAL.value), Decimal('24.5'))

        self.assertEqual(data.get(FieldName.GRID_FREQ_MIN_VALUE.value), Decimal('48'))
        self.assertEqual(data.get(FieldName.GRID_FREQ_MAX_VALUE.value), Decimal('52'))

        self.assertEqual(data.get(FieldName.WIFI_NAME.value), "MyHomeSSID")


    async def test_ep600_invalid_bool(self):
        self.ble_mock.add_r_int(2011, 5)

        device = EP600()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertIsNotNone(data)

        self.assertIsNone(data.get(FieldName.CTRL_AC.value))
