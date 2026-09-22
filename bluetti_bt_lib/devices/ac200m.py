from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC200M(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(
                    name=FieldName.AC_1_O_V,
                    address=71,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.AC_I_P_TOTAL,
                    address=37,
                ),
                UIntField(
                    name=FieldName.AC_O_F,
                    address=74,
                    multiplier=0.1,
                ),
                SelectField(
                    name=FieldName.AC_O_MODE,
                    address=70,
                    e=OutputMode,
                ),
                UIntField(
                    name=FieldName.AC_O_P_TOTAL,
                    address=38,
                ),
                SwitchField(
                    name=FieldName.AC_O_SWITCH,
                    address=3007,
                ),
                UIntField(
                    name=FieldName.B_SOC_TOTAL,
                    address=43,
                    min=0,
                    max=100,
                ),
                SelectField(
                    name=FieldName.D_DISPLAY_MODE,
                    address=3061,
                    e=DisplayMode,
                ),
                StringField(
                    name=FieldName.D_INVERTER_TYPE,
                    address=10,
                    size=6,
                ),
                SwitchField(
                    name=FieldName.D_POWER_OFF,
                    address=3060,
                ),
                SerialNumberField(
                    name=FieldName.D_SERIAL,
                    address=17,
                ),
                UIntField(
                    name=FieldName.DC_I_P_TOTAL,
                    address=36,
                ),
                UIntField(
                    name=FieldName.DC_I_V,
                    address=86,
                    multiplier=0.01,
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=39,
                ),
                SwitchField(
                    name=FieldName.DC_O_SWITCH,
                    address=3008,
                ),
                UIntField(
                    name=FieldName.PV_1_I_C,
                    address=88,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.PV_1_I_P,
                    address=87,
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 1
