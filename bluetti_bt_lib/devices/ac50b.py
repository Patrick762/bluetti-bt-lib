from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC50B(BluettiDevice):
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
                TimeField(
                    name=FieldName.D_TIME_REMAINING,
                    address=104,
                    sensor="duration",
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=140,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
            ]
        )
