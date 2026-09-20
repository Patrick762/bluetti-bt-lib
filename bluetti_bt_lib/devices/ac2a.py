from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC2A(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
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
                BoolField(
                    FieldName.AC_O_SWITCH,
                    2011,
                ),
                BoolField(
                    FieldName.AC_POWER_LIFTING_SWITCH,
                    2021,
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
                BoolField(
                    FieldName.DC_O_SWITCH,
                    2012,
                ),
                UIntField(
                    FieldName.PV_I_E_TOTAL,
                    154,
                    unit="kWh",
                    sensor="energy",
                    state_type="total_increasing",
                ),
            ]
        )
