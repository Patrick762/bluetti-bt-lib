from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EP500(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_1_O_V, 71),
                UIntField(FieldName.AC_I_F, 80),
                UIntField(FieldName.AC_1_I_V, 77),
                UIntField(FieldName.AC_I_P_TOTAL, 37),
                UIntField(FieldName.AC_O_F, 74),
                EnumField(FieldName.AC_O_MODE, 70),
                UIntField(FieldName.AC_O_P_TOTAL, 38),
                BoolField(FieldName.AC_O_SWITCH, 3007),
                EnumField(FieldName.AC_UPS_MODE, 3001),
                UIntField(FieldName.B_SOC_HIGH, 3016),
                UIntField(FieldName.B_SOC_LOW, 3015),
                UIntField(FieldName.B_SOC_TOTAL, 43),
                EnumField(FieldName.D_DISPLAY_MODE, 3061),
                StringField(FieldName.D_INVERTER_TYPE, 10),
                SerialNumberField(FieldName.D_SERIAL, 17),
                BoolField(FieldName.D_SPLIT_PHASE_SWITCH, 3004),
                EnumField(FieldName.D_SPLIT_PHASE_MODE, 3005),
                UIntField(FieldName.DC_I_P_TOTAL, 36),
                UIntField(FieldName.DC_O_P_TOTAL, 39),
                BoolField(FieldName.DC_O_SWITCH, 3008),
                UIntField(FieldName.PV_1_I_C, 88),
                UIntField(FieldName.PV_1_I_P, 87),
                UIntField(FieldName.PV_1_I_V, 86),
            ]
        )
