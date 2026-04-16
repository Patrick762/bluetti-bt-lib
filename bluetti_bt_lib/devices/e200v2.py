from ..base_devices import BaseDeviceV2
from ..fields import FieldName, UIntField, DecimalField


class E200V2(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.TIME_REMAINING, 104, 0, multiplier=1/60),
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                DecimalField(FieldName.BATTERY_VOLTAGE, 152, 2),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 1),
                DecimalField(FieldName.AC_INPUT_CURRENT, 1315, 1),
                DecimalField(FieldName.AC_OUTPUT_CURRENT, 1432, 1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1470, 1),
            ],
        )
