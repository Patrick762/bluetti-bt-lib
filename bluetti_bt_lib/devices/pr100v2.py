from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class PR100V2(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(
                    FieldName.AC_1_I_V,
                    1314,
                    unit="V",
                    sensor="voltage",
                    state_type="measurement",
                ),
                UIntField(
                    FieldName.AC_I_P_TOTAL,
                    146,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    FieldName.AC_O_P_TOTAL,
                    142,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    FieldName.B_SOC_TOTAL,
                    102,
                    unit="%",
                    sensor="battery",
                    state_type="measurement",
                ),
                SwapStringField(
                    FieldName.D_INVERTER_TYPE,
                    110,
                ),
                SerialNumberField(
                    FieldName.D_SERIAL,
                    116,
                ),
                UIntField(
                    FieldName.DC_I_P_TOTAL,
                    144,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    FieldName.DC_O_P_TOTAL,
                    140,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
            ]
        )
