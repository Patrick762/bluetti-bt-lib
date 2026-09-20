from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EB3A(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                SelectField(
                    name=FieldName.AC_ECO_MODE,
                    address=3064,
                    e=EcoMode,
                ),
                SwitchField(
                    name=FieldName.AC_ECO_SWITCH,
                    address=3063,
                ),
                UIntField(
                    name=FieldName.AC_1_I_V,
                    address=77,
                    multiplier=0.1,
                    unit="V",
                    sensor="voltage",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.AC_I_P_TOTAL,
                    address=37,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.AC_O_P_TOTAL,
                    address=38,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                SwitchField(
                    name=FieldName.AC_O_SWITCH,
                    address=3007,
                ),
                SwitchField(
                    name=FieldName.AC_POWER_LIFTING_SWITCH,
                    address=3066,
                ),
                UIntField(
                    name=FieldName.B_SOC_TOTAL,
                    address=43,
                    unit="%",
                    sensor="battery",
                    state_type="measurement",
                    min=0,
                    max=100,
                ),
                SelectField(
                    name=FieldName.D_CHARGING_MODE,
                    address=3065,
                    e=ChargingMode,
                ),
                StringField(
                    name=FieldName.D_INVERTER_TYPE,
                    address=10,
                    size=6,
                ),
                SelectField(
                    name=FieldName.D_LED_MODE,
                    address=3034,
                    e=LedMode,
                ),
                SwitchField(
                    name=FieldName.D_POWER_OFF,
                    address=3060,
                ),
                SerialNumberField(
                    name=FieldName.D_SERIAL,
                    address=17,
                ),
                VersionField(
                    name=FieldName.D_VER_ARM,
                    address=23,
                ),
                VersionField(
                    name=FieldName.D_VER_DSP,
                    address=25,
                ),
                UIntField(
                    name=FieldName.DC_I_P_TOTAL,
                    address=36,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.DC_I_V,
                    address=86,
                    multiplier=0.01,
                    unit="V",
                    sensor="voltage",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=39,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                SwitchField(
                    name=FieldName.DC_O_SWITCH,
                    address=3008,
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 1
