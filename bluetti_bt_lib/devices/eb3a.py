from ..base_devices import BaseDeviceV1
from ..fields import FieldName, SwitchField, SelectField
from ..enums import LedMode, ChargingMode


class EB3A(BaseDeviceV1):
    def __init__(self):
        super().__init__(
            [
                SwitchField(FieldName.CTRL_AC, 3007),
                SwitchField(FieldName.CTRL_DC, 3008),
                SelectField(FieldName.CTRL_LED_MODE, 3034, LedMode),
                SwitchField(FieldName.CTRL_POWER_OFF, 3060),
                SelectField(FieldName.CTRL_CHARGING_MODE, 3065, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 3066),
            ],
        )
