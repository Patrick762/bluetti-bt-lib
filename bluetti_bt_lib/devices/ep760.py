from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EP760(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_1_O_C, 1512),
                UIntField(FieldName.AC_1_O_P, 1510),
                UIntField(FieldName.AC_1_O_V, 1511),
                UIntField(FieldName.AC_I_F, 1300),
                UIntField(FieldName.AC_1_I_C, 1315),
                UIntField(FieldName.AC_1_I_P, 1313),
                UIntField(FieldName.AC_1_I_V, 1314),
                UIntField(FieldName.AC_O_F, 1500),
                UIntField(FieldName.B_SOC_TOTAL, 102),
                SwapStringField(FieldName.D_INVERTER_TYPE, 110),
                SerialNumberField(FieldName.D_SERIAL, 116),
                UIntField(FieldName.G_I_F, 1300),
                UIntField(FieldName.PV_1_I_C, 1214),
                UIntField(FieldName.PV_1_I_P, 1212),
                UIntField(FieldName.PV_1_I_V, 1213),
                UIntField(FieldName.PV_2_I_C, 1222),
                UIntField(FieldName.PV_2_I_P, 1220),
                UIntField(FieldName.PV_2_I_V, 1221),
                UIntField(FieldName.PV_3_I_C, 1230),
                UIntField(FieldName.PV_3_I_P, 1228),
                UIntField(FieldName.PV_3_I_V, 1229),
            ]
        )
