from ..base_devices import BaseDeviceV2
from ..enums import LedPanelState
from ..fields import EnumField, FieldName, UIntField, SwitchField


class AC60(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                UIntField(FieldName.AC_INPUT_VOLTAGE, 1314),
                SwitchField(FieldName.CTRL_AC, 2011),
                SwitchField(FieldName.CTRL_DC, 2012),
                EnumField(FieldName.LED_MODE, 2007, LedPanelState),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 2021),
            ],
        )
