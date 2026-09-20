from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class Handsfree1(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(
                    name=FieldName.AC_1_O_V,
                    address=1511,
                    multiplier=0.1,
                    unit="V",
                    sensor="voltage",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.AC_I_F,
                    address=1300,
                    multiplier=0.1,
                    unit="Hz",
                    sensor="frequency",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.AC_1_I_C,
                    address=1315,
                    multiplier=0.1,
                    unit="A",
                    sensor="current",
                    state_type="measurement",
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
                    name=FieldName.AC_O_F,
                    address=1500,
                    multiplier=0.1,
                    unit="Hz",
                    sensor="frequency",
                ),
                UIntField(
                    name=FieldName.AC_O_P_TOTAL,
                    address=142,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
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
                UIntField(
                    name=FieldName.DC_I_C,
                    address=1214,
                    multiplier=0.1,
                    unit="A",
                    sensor="current",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.DC_I_P_TOTAL,
                    address=144,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.DC_I_V,
                    address=1213,
                    multiplier=0.1,
                    unit="V",
                    sensor="voltage",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=140,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.G_I_F,
                    address=1300,
                    multiplier=0.1,
                    unit="Hz",
                    sensor="frequency",
                    state_type="measurement",
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 2
