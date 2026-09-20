from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC2P(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
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
                BoolField(
                    name=FieldName.AC_O_SWITCH,
                    address=2011,
                ),
                BoolField(
                    name=FieldName.AC_POWER_LIFTING_SWITCH,
                    address=2021,
                ),
                UIntField(
                    name=FieldName.B_SOC_TOTAL,
                    address=102,
                    unit="%",
                    sensor="battery",
                    state_type="measurement",
                ),
                SwapStringField(
                    name=FieldName.D_INVERTER_TYPE,
                    address=110,
                ),
                SerialNumberField(
                    name=FieldName.D_SERIAL,
                    address=116,
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
                BoolField(
                    name=FieldName.DC_O_SWITCH,
                    address=2012,
                ),
                UIntField(
                    name=FieldName.PV_I_E_TOTAL,
                    address=154,
                    unit="kWh",
                    sensor="energy",
                    state_type="total_increasing",
                ),
            ]
        )
