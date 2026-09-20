from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC180T(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_1_O_V, 1511),
                UIntField(FieldName.AC_I_F, 1300),
                UIntField(FieldName.AC_1_I_C, 1315),
                UIntField(FieldName.AC_1_I_V, 1314),
                UIntField(FieldName.AC_I_P_TOTAL, 146),
                UIntField(FieldName.AC_O_F, 1500),
                UIntField(FieldName.AC_O_P_TOTAL, 142),
                UIntField(FieldName.B_SOC_TOTAL, 102),
                SwapStringField(FieldName.D_INVERTER_TYPE, 110),
                SerialNumberField(FieldName.D_SERIAL, 116),
                TimeField(FieldName.D_TIME_REMAINING, 104),
                UIntField(FieldName.DC_I_C, 1214),
                UIntField(FieldName.DC_I_P_TOTAL, 144),
                UIntField(FieldName.DC_I_V, 1213),
                UIntField(FieldName.DC_O_P_TOTAL, 140),
                UIntField(FieldName.G_I_F, 1300),
            ]
        )
