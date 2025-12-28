from ..base_devices import BaseDeviceV1
from ..fields import (
    FieldName,
    SwitchField,
    SelectField,
    VersionField,
    DecimalField,
)
from ..enums import EcoMode, LedMode, ChargingMode


class EB3A(BaseDeviceV1):
    def __init__(self):
        super().__init__(
            [
                VersionField(FieldName.VER_ARM, 23),
                VersionField(FieldName.VER_DSP, 25),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 77, 1),
                DecimalField(FieldName.DC_INPUT_VOLTAGE, 86, 2),
                SwitchField(FieldName.CTRL_AC, 3007),
                SwitchField(FieldName.CTRL_DC, 3008),
                SelectField(FieldName.CTRL_LED_MODE, 3034, LedMode),
                SwitchField(FieldName.CTRL_POWER_OFF, 3060),
                SwitchField(FieldName.CTRL_ECO, 3063),
                SelectField(FieldName.CTRL_ECO_TIME_MODE, 3064, EcoMode),
                SelectField(FieldName.CTRL_CHARGING_MODE, 3065, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 3066),
            ],
        )
