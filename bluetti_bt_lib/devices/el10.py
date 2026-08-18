from decimal import Decimal

from ..enums import EcoMode, DisplayMode, ChargingMode
from ..fields import (
    FieldName,
    UIntField,
    SelectField,
    SwitchField,
    DecimalField,
    VersionField,
    SwapStringField,
)
from ..base_devices import BaseDeviceV2


class EL10(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.TIME_REMAINING, 104, 0, 1 / Decimal(60)),
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 1),
                DecimalField(FieldName.AC_INPUT_CURRENT, 1315, 1),
                DecimalField(FieldName.AC_OUTPUT_VOLTAGE, 1511, 1),
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
                SelectField(FieldName.CTRL_DISPLAY_TIMEOUT, 2067, DisplayMode),
                VersionField(FieldName.VER_BMS, 6175),
            ],
        )