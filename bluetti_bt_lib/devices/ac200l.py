from ..base_devices import BaseDeviceV1
from ..fields import FieldName, EnumField, DecimalField, UIntField
from ..enums import OutputMode


class AC200L(BaseDeviceV1):
    def __init__(self):
        super().__init__(
            [
                EnumField(FieldName.AC_OUTPUT_MODE, 70, OutputMode),
                DecimalField(FieldName.INTERNAL_AC_VOLTAGE, 71, 1, 10),
                DecimalField(FieldName.INTERNAL_AC_FREQUENCY, 74, 2, 10),
                UIntField(FieldName.INTERNAL_DC_INPUT_VOLTAGE, 86, 0.1),
                DecimalField(FieldName.INTERNAL_DC_INPUT_POWER, 87, 1, 10),
                DecimalField(FieldName.INTERNAL_DC_INPUT_CURRENT, 88, 2),
            ],
        )
