from ..base_devices import BaseDeviceV2
from ..enums import ChargingMode
from ..fields import FieldName, UIntField, SwitchField, SelectField, DecimalField


class AC180P(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 1),
                SwitchField(FieldName.CTRL_AC, 2011),
                SwitchField(FieldName.CTRL_DC, 2012),
                SelectField(FieldName.CTRL_CHARGING_MODE, 2020, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 2021),
            ],
        )
