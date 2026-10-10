from decimal import Decimal

from ..base_devices import BaseDeviceV2
from ..enums import ChargingMode, EcoMode, UpsModeV2
from ..fields import (
    FieldName,
    UIntField,
    IntField,
    DecimalField,
    SwitchField,
    SelectField,
    SwapStringField,
    VersionField,
)


class FP(BaseDeviceV2):
    """FridgePower"""

    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.TIME_REMAINING, 104, 0, 1 / Decimal(60)),
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                # Signed, negative while power is drawn from the grid
                IntField(FieldName.AC_INPUT_POWER, 146, -1),
                VersionField(FieldName.VER_ARM, 1114),
                VersionField(FieldName.VER_DSP, 1117),
                DecimalField(FieldName.DC_INPUT_VOLTAGE, 1213, 1),
                DecimalField(FieldName.DC_INPUT_CURRENT, 1214, 1),
                DecimalField(FieldName.AC_INPUT_FREQUENCY, 1300, 1),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 1),
                # Signed like the input power
                IntField(FieldName.AC_INPUT_CURRENT, 1315, -0.1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                DecimalField(FieldName.AC_OUTPUT_VOLTAGE, 1511, 1),
                SelectField(FieldName.CTRL_UPS_MODE, 2005, UpsModeV2),
                SwitchField(FieldName.CTRL_AC, 2011),
                SwitchField(FieldName.CTRL_DC, 2012),
                SwitchField(FieldName.CTRL_ECO_DC, 2014),
                SelectField(FieldName.CTRL_ECO_TIME_MODE_DC, 2015, EcoMode),
                UIntField(FieldName.CTRL_ECO_MIN_POWER_DC, 2016),
                SwitchField(FieldName.CTRL_ECO_AC, 2017),
                SelectField(FieldName.CTRL_ECO_TIME_MODE_AC, 2018, EcoMode),
                UIntField(FieldName.CTRL_ECO_MIN_POWER_AC, 2019),
                SelectField(FieldName.CTRL_CHARGING_MODE, 2020, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 2021),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023),
                SwitchField(FieldName.CTRL_TIME_OF_USE, 2029),
                # Called "Grid Self-Adaption" in the app
                SwitchField(FieldName.CTRL_GRID_STABILIZING, 2225),
                VersionField(FieldName.VER_BMS, 6175),
                SwapStringField(FieldName.WIFI_NAME, 12002, 16),
            ],
        )
