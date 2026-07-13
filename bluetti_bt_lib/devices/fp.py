from ..base_devices import BaseDeviceV2
from ..enums import ChargingMode, EcoMode, UpsMode
from ..fields import FieldName, UIntField, IntField, DecimalField, SwitchField, SelectField


class FP(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.TIME_REMAINING, 104, 0, 1/60, precision=2),
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                IntField(FieldName.AC_INPUT_POWER, 146, multiplier=-1),
                DecimalField(FieldName.DC_INPUT_VOLTAGE, 1213, 1),
                DecimalField(FieldName.DC_INPUT_CURRENT, 1214, 1),
                DecimalField(FieldName.AC_INPUT_FREQUENCY, 1300, 1),
                UIntField(FieldName.AC_INPUT_VOLTAGE, 1314, 0.1),
                IntField(FieldName.AC_INPUT_CURRENT, 1315, multiplier=-0.1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                DecimalField(FieldName.AC_OUTPUT_VOLTAGE, 1511, 1),
                SwitchField(FieldName.CTRL_AC, 2011),
                SwitchField(FieldName.CTRL_DC, 2012),
                SwitchField(FieldName.CTRL_ECO_AC, 2017),
                SelectField(FieldName.CTRL_ECO_TIME_MODE_AC, 2018, EcoMode),
                UIntField(FieldName.CTRL_ECO_MIN_POWER_AC, 2019),
                SelectField(FieldName.CTRL_CHARGING_MODE, 2020, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 2021),
                SelectField(FieldName.CTRL_UPS_MODE, 3001, UpsMode),
            ],
        )
