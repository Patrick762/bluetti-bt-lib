from ..base_devices import BaseDeviceV2
from ..enums import ChargingMode, DisplayMode, WorkingMode
from ..fields import (
    FieldName,
    UIntField,
    NumberField,
    DecimalField,
    SwitchField,
    SelectField,
)


class AP300(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.TIME_REMAINING, 104, 1),
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                DecimalField(FieldName.AC_INPUT_FREQUENCY, 1300, 1),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 1),
                DecimalField(FieldName.AC_INPUT_CURRENT, 1315, 1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                DecimalField(FieldName.AC_OUTPUT_VOLTAGE, 1511, 1),
                SwitchField(FieldName.CTRL_AC, 2011),
                SwitchField(FieldName.CTRL_DC, 2012),
                SwitchField(FieldName.CTRL_ECO_DC, 2014),
                SwitchField(FieldName.CTRL_ECO_AC, 2017),
                SelectField(FieldName.CTRL_CHARGING_MODE, 2020, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 2021),
                NumberField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100),
                NumberField(FieldName.BATTERY_SOC_RANGE_END, 2023, min=0, max=100),
                SelectField(FieldName.CTRL_WORKING_MODE, 2005, WorkingMode),
                SwitchField(FieldName.CTRL_CHARGE_FROM_GRID, 2207),
                SelectField(FieldName.CTRL_DISPLAY_TIMEOUT, 2067, DisplayMode),
            ],
        )
