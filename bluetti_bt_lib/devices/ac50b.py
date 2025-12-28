from ..base_devices import BaseDeviceV2
from ..fields import FieldName, UIntField, DecimalField


class AC50B(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.TIME_REMAINING, 104, 1),
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.AC_INPUT_POWER, 146),
            ],
        )
