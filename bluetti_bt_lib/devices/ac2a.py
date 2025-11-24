from ..base_devices import BaseDeviceV2
from ..fields import FieldName, UIntField, DecimalField, BoolField


class AC2A(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                DecimalField(FieldName.POWER_GENERATION, 154),
                BoolField(FieldName.AC_OUTPUT_ON, 1509),
                BoolField(FieldName.DC_OUTPUT_ON, 2012),
                BoolField(FieldName.POWER_LIFTING_ON, 2021),
            ],
        )
