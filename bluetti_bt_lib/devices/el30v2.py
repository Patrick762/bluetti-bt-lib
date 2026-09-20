from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EL30V2(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                SelectField(
                    name=FieldName.AC_ECO_MODE,
                    address=2018,
                    e=EcoMode,
                    category="config",
                ),
                SwitchField(
                    name=FieldName.AC_ECO_SWITCH,
                    address=2017,
                    category="config",
                ),
                UIntField(
                    name=FieldName.AC_1_I_V,
                    address=1314,
                    multiplier=0.1,
                    unit="V",
                    sensor="voltage",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.AC_I_P_TOTAL,
                    address=146,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.AC_O_P_TOTAL,
                    address=142,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                SwitchField(
                    name=FieldName.AC_O_SWITCH,
                    address=2011,
                ),
                SwitchField(
                    name=FieldName.AC_POWER_LIFTING_SWITCH,
                    address=2021,
                    category="config",
                ),
                UIntField(
                    name=FieldName.B_SOC_TOTAL,
                    address=102,
                    unit="%",
                    sensor="battery",
                    state_type="measurement",
                    min=0,
                    max=100,
                ),
                SelectField(
                    name=FieldName.D_CHARGING_MODE,
                    address=2020,
                    e=ChargingMode,
                    category="config",
                ),
                SwapStringField(
                    name=FieldName.D_INVERTER_TYPE,
                    address=110,
                    size=6,
                    category="diagnostic",
                ),
                SerialNumberField(
                    name=FieldName.D_SERIAL,
                    address=116,
                    category="diagnostic",
                ),
                TimeField(
                    name=FieldName.D_TIME_REMAINING,
                    address=104,
                    sensor="duration",
                ),
                SelectField(
                    name=FieldName.DC_ECO_MODE,
                    address=2015,
                    e=EcoMode,
                    category="config",
                ),
                SwitchField(
                    name=FieldName.DC_ECO_SWITCH,
                    address=2014,
                    category="config",
                ),
                UIntField(
                    name=FieldName.DC_I_P_TOTAL,
                    address=144,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=140,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                SwitchField(
                    name=FieldName.DC_O_SWITCH,
                    address=2012,
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 2
