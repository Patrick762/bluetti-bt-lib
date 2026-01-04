from ..base_devices import BaseDeviceV1
from ..fields import (
    FieldName,
    EnumField,
    DecimalField,
    SwitchField,
    SelectField,
    UIntField,
    VersionField,
)
from ..enums import OutputMode, DisplayMode, UpsMode


class AC200L(BaseDeviceV1):
    def __init__(self):
        super().__init__(
            [
                VersionField(FieldName.VER_ARM, 23),
                VersionField(FieldName.VER_DSP, 25),
                EnumField(FieldName.AC_OUTPUT_MODE, 70, OutputMode),
                DecimalField(FieldName.INTERNAL_AC_VOLTAGE, 71, 1, 10),
                DecimalField(FieldName.INTERNAL_AC_FREQUENCY, 74, 2, 10),
                DecimalField(FieldName.INTERNAL_DC_INPUT_VOLTAGE, 86, 1),
                DecimalField(FieldName.INTERNAL_DC_INPUT_POWER, 87, 1, 10),
                DecimalField(FieldName.INTERNAL_DC_INPUT_CURRENT, 88, 2),
                SelectField(FieldName.CTRL_UPS_MODE, 3001, UpsMode),
                SwitchField(FieldName.CTRL_AC, 3007),
                SwitchField(FieldName.CTRL_DC, 3008),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 3015, min=0, max=100),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 3016, min=0, max=100),
                SwitchField(FieldName.CTRL_POWER_OFF, 3060),
                SelectField(FieldName.CTRL_DISPLAY_TIMEOUT, 3061, DisplayMode),
            ],
        )
