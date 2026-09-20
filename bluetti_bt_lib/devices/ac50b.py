from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC50B(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_I_P_TOTAL, 146),
                UIntField(FieldName.AC_O_P_TOTAL, 142),
                UIntField(FieldName.B_SOC_TOTAL, 102),
                SwapStringField(FieldName.D_INVERTER_TYPE, 110),
                SerialNumberField(FieldName.D_SERIAL, 116),
                TimeField(FieldName.D_TIME_REMAINING, 104),
                UIntField(FieldName.DC_O_P_TOTAL, 140),
            ]
        )
