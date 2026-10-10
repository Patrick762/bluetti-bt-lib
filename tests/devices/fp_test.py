import asyncio
from decimal import Decimal
import unittest

from bluetti_bt_lib.utils.bleak_client_mock import ClientMockNoEncryption
from bluetti_bt_lib.devices import FP
from bluetti_bt_lib.enums import ChargingMode, EcoMode, UpsModeV2
from bluetti_bt_lib import DeviceReader, FieldName


class TestFP(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._createMock()

    def _createMock(self):
        self.ble_mock = ClientMockNoEncryption()

        # Battery SOC
        self.ble_mock.add_r_int(102, 90)
        # Time remaining (minutes)
        self.ble_mock.add_r_int(104, 2292)
        # Device type
        self.ble_mock.add_r_sstr(110, "FP", 6)
        # Device SN
        self.ble_mock.add_r_sn(116, 2600000000001)

        # DC Output Power
        self.ble_mock.add_r_int(140, 0)
        # AC Output Power
        self.ble_mock.add_r_int(142, 64)
        # DC Input Power
        self.ble_mock.add_r_int(144, 0)
        # AC Input Power (-64, grid passthrough)
        self.ble_mock.add_r_int(146, 0xFFC0)

        # ARM version (v10014.01.14)
        self.ble_mock.add_r_int(1114, 0x0452)
        self.ble_mock.add_r_int(1115, 0x05F8)
        # DSP version (v10013.01.10)
        self.ble_mock.add_r_int(1117, 0xDD3E)
        self.ble_mock.add_r_int(1118, 0x05F7)

        # DC Input Voltage
        self.ble_mock.add_r_int(1213, 365)
        # DC Input Current
        self.ble_mock.add_r_int(1214, 82)

        # AC Input Frequency
        self.ble_mock.add_r_int(1300, 600)
        # AC Input Voltage
        self.ble_mock.add_r_int(1314, 1202)
        # AC Input Current (-0.9 A)
        self.ble_mock.add_r_int(1315, 0xFFF7)

        # AC Output Frequency
        self.ble_mock.add_r_int(1500, 600)
        # AC Output Voltage
        self.ble_mock.add_r_int(1511, 1209)

        # UPS mode
        self.ble_mock.add_r_int(2005, 4)

        # Control AC
        self.ble_mock.add_r_int(2011, 1)
        # Control DC
        self.ble_mock.add_r_int(2012, 1)
        # ECO DC
        self.ble_mock.add_r_int(2014, 0)
        self.ble_mock.add_r_int(2015, 4)
        self.ble_mock.add_r_int(2016, 5)
        # ECO AC
        self.ble_mock.add_r_int(2017, 1)
        self.ble_mock.add_r_int(2018, 4)
        self.ble_mock.add_r_int(2019, 10)
        # Charging mode
        self.ble_mock.add_r_int(2020, 0)
        # Power lifting
        self.ble_mock.add_r_int(2021, 1)

        # Battery SOC Range Start
        self.ble_mock.add_r_int(2022, 20)
        # Battery SOC Range End
        self.ble_mock.add_r_int(2023, 80)

        # Time of use
        self.ble_mock.add_r_int(2029, 1)

        # Grid self-adaption
        self.ble_mock.add_r_int(2225, 1)

        # BMS version (v10000.01.12)
        self.ble_mock.add_r_int(6175, 0xE170)
        self.ble_mock.add_r_int(6176, 0x05F5)

        # WiFi SSID
        self.ble_mock.add_r_sstr(12002, "MyHomeSSID", 16)

    async def test_fp(self):
        device = FP()
        reader = DeviceReader(
            "00:11:00:11:00:11",
            device,
            asyncio.Future,
            ble_client=self.ble_mock,
        )

        data = await reader.read()

        self.assertIsNotNone(data)

        self.assertEqual(data.get(FieldName.BATTERY_SOC.value), 90)
        self.assertEqual(data.get(FieldName.DEVICE_TYPE.value), "FP")
        self.assertEqual(data.get(FieldName.DEVICE_SN.value), 2600000000001)

        self.assertEqual(
            data.get(FieldName.TIME_REMAINING.value), Decimal(2292) * (1 / Decimal(60))
        )

        self.assertEqual(data.get(FieldName.DC_OUTPUT_POWER.value), 0)
        self.assertEqual(data.get(FieldName.AC_OUTPUT_POWER.value), 64)
        self.assertEqual(data.get(FieldName.DC_INPUT_POWER.value), 0)
        self.assertEqual(data.get(FieldName.AC_INPUT_POWER.value), 64)

        self.assertEqual(data.get(FieldName.DC_INPUT_VOLTAGE.value), Decimal("36.5"))
        self.assertEqual(data.get(FieldName.DC_INPUT_CURRENT.value), Decimal("8.2"))

        self.assertEqual(data.get(FieldName.AC_INPUT_FREQUENCY.value), Decimal("60.0"))
        self.assertEqual(data.get(FieldName.AC_INPUT_VOLTAGE.value), Decimal("120.2"))
        self.assertEqual(data.get(FieldName.AC_INPUT_CURRENT.value), 0.9)
        self.assertEqual(data.get(FieldName.AC_OUTPUT_FREQUENCY.value), Decimal("60.0"))
        self.assertEqual(data.get(FieldName.AC_OUTPUT_VOLTAGE.value), Decimal("120.9"))

        self.assertEqual(data.get(FieldName.CTRL_UPS_MODE.value), UpsModeV2.STANDARD)
        self.assertEqual(data.get(FieldName.CTRL_AC.value), True)
        self.assertEqual(data.get(FieldName.CTRL_DC.value), True)
        self.assertEqual(data.get(FieldName.CTRL_ECO_DC.value), False)
        self.assertEqual(
            data.get(FieldName.CTRL_ECO_TIME_MODE_DC.value), EcoMode.HOURS4
        )
        self.assertEqual(data.get(FieldName.CTRL_ECO_MIN_POWER_DC.value), 5)
        self.assertEqual(data.get(FieldName.CTRL_ECO_AC.value), True)
        self.assertEqual(
            data.get(FieldName.CTRL_ECO_TIME_MODE_AC.value), EcoMode.HOURS4
        )
        self.assertEqual(data.get(FieldName.CTRL_ECO_MIN_POWER_AC.value), 10)
        self.assertEqual(
            data.get(FieldName.CTRL_CHARGING_MODE.value), ChargingMode.STANDARD
        )

        self.assertEqual(data.get(FieldName.CTRL_POWER_LIFTING.value), True)

        self.assertEqual(data.get(FieldName.BATTERY_SOC_RANGE_START.value), 20)
        self.assertEqual(data.get(FieldName.BATTERY_SOC_RANGE_END.value), 80)

        self.assertEqual(data.get(FieldName.CTRL_TIME_OF_USE.value), True)

        self.assertEqual(data.get(FieldName.CTRL_GRID_STABILIZING.value), True)

        self.assertEqual(data.get(FieldName.VER_ARM.value), Decimal("1001401.14"))
        self.assertEqual(data.get(FieldName.VER_DSP.value), Decimal("1001301.10"))
        self.assertEqual(data.get(FieldName.VER_BMS.value), Decimal("1000001.12"))

        self.assertEqual(data.get(FieldName.WIFI_NAME.value), "MyHomeSSID")
