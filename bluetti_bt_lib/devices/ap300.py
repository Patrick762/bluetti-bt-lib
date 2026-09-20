from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AP300(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_1_I_V, 1314),
                UIntField(FieldName.AC_I_P_TOTAL, 146),
                UIntField(FieldName.AC_O_P_TOTAL, 142),
                UIntField(FieldName.B_SOC_TOTAL, 102),
                SwapStringField(FieldName.D_INVERTER_TYPE, 110),
                SerialNumberField(FieldName.D_SERIAL, 116),
                UIntField(FieldName.DC_I_P_TOTAL, 144),
                UIntField(FieldName.DC_O_P_TOTAL, 140),
            ]
        )
