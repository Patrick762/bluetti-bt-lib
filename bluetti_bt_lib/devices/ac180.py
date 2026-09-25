from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC180(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(
                    name=FieldName.AC_1_O_V,
                    address=1511,
                    multiplier=0.1,
                ),
                SelectField(
                    name=FieldName.AC_ECO_MODE,
                    address=2018,
                    e=EcoMode,
                ),
                SwitchField(
                    name=FieldName.AC_ECO_SWITCH,
                    address=2017,
                ),
                UIntField(
                    name=FieldName.AC_I_F,
                    address=1300,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.AC_1_I_C,
                    address=1315,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.AC_1_I_V,
                    address=1314,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.AC_I_P_TOTAL,
                    address=146,
                ),
                UIntField(
                    name=FieldName.AC_O_F,
                    address=1500,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.AC_O_P_TOTAL,
                    address=142,
                ),
                SwitchField(
                    name=FieldName.AC_O_SWITCH,
                    address=2011,
                ),
                SwitchField(
                    name=FieldName.AC_POWER_LIFTING_SWITCH,
                    address=2021,
                ),
                UIntField(
                    name=FieldName.B_SOC_TOTAL,
                    address=102,
                    min=0,
                    max=100,
                ),
                VersionField(
                    name=FieldName.B_VER_BMS,
                    address=6175,
                ),
                SelectField(
                    name=FieldName.D_CHARGING_MODE,
                    address=2020,
                    e=ChargingMode,
                ),
                SwapStringField(
                    name=FieldName.D_INVERTER_TYPE,
                    address=110,
                    size=6,
                ),
                SerialNumberField(
                    name=FieldName.D_SERIAL,
                    address=116,
                ),
                SelectField(
                    name=FieldName.DC_ECO_MODE,
                    address=2015,
                    e=EcoMode,
                ),
                SwitchField(
                    name=FieldName.DC_ECO_SWITCH,
                    address=2014,
                ),
                UIntField(
                    name=FieldName.DC_I_C,
                    address=1214,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.DC_I_P_TOTAL,
                    address=144,
                ),
                UIntField(
                    name=FieldName.DC_I_V,
                    address=1213,
                    multiplier=0.1,
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=140,
                ),
                SwitchField(
                    name=FieldName.DC_O_SWITCH,
                    address=2012,
                ),
                UIntField(
                    name=FieldName.G_I_F,
                    address=1300,
                    multiplier=0.1,
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 2
