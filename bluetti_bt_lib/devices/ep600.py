from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EP600(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_1_O_C, 1512),
                UIntField(FieldName.AC_1_O_P, 1510),
                UIntField(FieldName.AC_1_O_V, 1511),
                UIntField(FieldName.AC_2_O_C, 1519),
                UIntField(FieldName.AC_2_O_P, 1517),
                UIntField(FieldName.AC_2_O_V, 1518),
                UIntField(FieldName.AC_3_O_C, 1526),
                UIntField(FieldName.AC_3_O_P, 1524),
                UIntField(FieldName.AC_3_O_V, 1525),
                UIntField(FieldName.AC_I_F, 1300),
                UIntField(FieldName.AC_1_I_C, 1315),
                UIntField(FieldName.AC_1_I_P, 1313),
                UIntField(FieldName.AC_1_I_V, 1314),
                UIntField(FieldName.AC_2_I_C, 1321),
                UIntField(FieldName.AC_2_I_P, 1319),
                UIntField(FieldName.AC_2_I_V, 1320),
                UIntField(FieldName.AC_3_I_C, 1327),
                UIntField(FieldName.AC_3_I_P, 1325),
                UIntField(FieldName.AC_3_I_V, 1326),
                UIntField(FieldName.AC_O_F, 1500),
                BoolField(FieldName.AC_O_SWITCH, 2011),
                UIntField(FieldName.B_SOC_HIGH, 2023),
                UIntField(FieldName.B_SOC_LOW, 2022),
                UIntField(FieldName.B_SOC_TOTAL, 102),
                StringField(FieldName.B_TYPE, 6101),
                SwapStringField(FieldName.D_INVERTER_TYPE, 110),
                SerialNumberField(FieldName.D_SERIAL, 116),
                UIntField(FieldName.PV_1_I_C, 1214),
                UIntField(FieldName.PV_1_I_P, 1212),
                UIntField(FieldName.PV_1_I_V, 1213),
                UIntField(FieldName.PV_2_I_C, 1222),
                UIntField(FieldName.PV_2_I_P, 1220),
                UIntField(FieldName.PV_2_I_V, 1221),
                UIntField(FieldName.PV_3_I_C, 1230),
                UIntField(FieldName.PV_3_I_P, 1228),
                UIntField(FieldName.PV_3_I_V, 1229),
                UIntField(FieldName.PV_4_I_C, 1238),
                UIntField(FieldName.PV_4_I_P, 1236),
                UIntField(FieldName.PV_4_I_V, 1237),
                UIntField(FieldName.PV_5_I_C, 1246),
                UIntField(FieldName.PV_5_I_P, 1244),
                UIntField(FieldName.PV_5_I_V, 1245),
            ]
        )
