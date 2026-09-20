from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC180(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_1_O_V, 1511),
                EnumField(FieldName.AC_ECO_MODE, 2018),
                BoolField(FieldName.AC_ECO_SWITCH, 2017),
                UIntField(FieldName.AC_I_F, 1300),
                UIntField(FieldName.AC_1_I_C, 1315),
                UIntField(FieldName.AC_1_I_V, 1314),
                UIntField(FieldName.AC_I_P_TOTAL, 146),
                UIntField(FieldName.AC_O_F, 1500),
                UIntField(FieldName.AC_O_P_TOTAL, 142),
                BoolField(FieldName.AC_O_SWITCH, 2011),
                BoolField(FieldName.AC_POWER_LIFTING_SWITCH, 2021),
                UIntField(FieldName.B_SOC_TOTAL, 102),
                VersionField(FieldName.B_VER_BMS, 6175),
                EnumField(FieldName.D_CHARGING_MODE, 2020),
                SwapStringField(FieldName.D_INVERTER_TYPE, 110),
                SerialNumberField(FieldName.D_SERIAL, 116),
                EnumField(FieldName.DC_ECO_MODE, 2015),
                BoolField(FieldName.DC_ECO_SWITCH, 2014),
                UIntField(FieldName.DC_I_C, 1214),
                UIntField(FieldName.DC_I_P_TOTAL, 144),
                UIntField(FieldName.DC_I_V, 1213),
                UIntField(FieldName.DC_O_P_TOTAL, 140),
                BoolField(FieldName.DC_O_SWITCH, 2012),
                UIntField(FieldName.G_I_F, 1300),
            ]
        )
