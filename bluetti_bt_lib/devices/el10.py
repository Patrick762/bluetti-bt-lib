"""EL10 device. BaseDeviceV2, encryption required. Single source of reference for EL10.

Attributes (addresses in parentheses):
  Status: TIME_REMAINING(104), DC/AC_OUTPUT_POWER(140,142), DC/AC_INPUT_POWER(144,146),
          POWER_GENERATION(154), DC_INPUT_VOLTAGE/CURRENT(1213,1214), AC_INPUT_FREQUENCY(1300),
          AC_INPUT_VOLTAGE/CURRENT(1314,1315), AC_OUTPUT_FREQUENCY(1500), AC_OUTPUT_VOLTAGE(1511).
  Controls: CTRL_LED_MODE(2007), CTRL_AC(2011), CTRL_DC(2012), CTRL_ECO_DC/AC(2014,2017),
            CTRL_ECO_TIME_MODE_DC/AC(2015,2018), CTRL_ECO_MIN_POWER_DC(2016), CTRL_ECO_MIN_POWER_AC(2019),
            CTRL_CHARGING_MODE(2020), CTRL_POWER_LIFTING(2021),
            BATTERY_SOC_RANGE_START/END(2022,2023).
  BMS: VER_BMS(6175).

Register block ranges: 101–161 (status), 1101–1161 (device/SN), 1201–1281 (DC/AC input),
1301–1441 (AC in/out), 2001–2081 (controls), 6001–6201 (BMS), 6301–7001 & 11011 (extended).

LED torch (CTRL_LED_MODE at 2007): EL10LedMode OFF=0, COLD=1, WARM=2, SOS=3. Read/write;
write confirmed. Other LED-related addresses from readall diff: 103 (block 101) = on/off only
(1=off, 2=on), read-only; 161 = correlates, not exposed.

Per manual: ECO time 1h–4h (EcoMode); ECO min power DC 5–10W, AC 15–30W.
"""

from ..base_devices import BaseDeviceV2
from ..enums import ChargingMode, EcoMode, EL10LedMode
from ..fields import (
    FieldName,
    UIntField,
    DecimalField,
    SwitchField,
    SelectField,
    VersionField,
)


class EL10(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.TIME_REMAINING, 104, 1),
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                DecimalField(FieldName.POWER_GENERATION, 154, 1),
                DecimalField(FieldName.DC_INPUT_VOLTAGE, 1213, 1),
                DecimalField(FieldName.DC_INPUT_CURRENT, 1214, 1),
                DecimalField(FieldName.AC_INPUT_FREQUENCY, 1300, 1),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 1),
                DecimalField(FieldName.AC_INPUT_CURRENT, 1315, 1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                DecimalField(FieldName.AC_OUTPUT_VOLTAGE, 1511, 1),
                SelectField(FieldName.CTRL_LED_MODE, 2007, EL10LedMode),  # LED torch: off=0, cold=1, warm=2, sos=3
                SwitchField(FieldName.CTRL_AC, 2011),
                SwitchField(FieldName.CTRL_DC, 2012),
                SwitchField(FieldName.CTRL_ECO_DC, 2014),
                SelectField(FieldName.CTRL_ECO_TIME_MODE_DC, 2015, EcoMode),  # 1h–4h
                UIntField(FieldName.CTRL_ECO_MIN_POWER_DC, 2016, min=5, max=10, writeable=True),  # 5W–10W
                SwitchField(FieldName.CTRL_ECO_AC, 2017),
                SelectField(FieldName.CTRL_ECO_TIME_MODE_AC, 2018, EcoMode),  # 1h–4h
                UIntField(FieldName.CTRL_ECO_MIN_POWER_AC, 2019, min=15, max=30, writeable=True),  # 15W–30W
                SelectField(FieldName.CTRL_CHARGING_MODE, 2020, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 2021),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023),
                VersionField(FieldName.VER_BMS, 6175),
            ],
        )
