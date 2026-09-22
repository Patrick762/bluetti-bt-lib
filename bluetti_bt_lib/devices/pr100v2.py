from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class PR100V2(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
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
                    name=FieldName.AC_O_P_TOTAL,
                    address=142,
                ),
                UIntField(
                    name=FieldName.B_SOC_TOTAL,
                    address=102,
                    min=0,
                    max=100,
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
                UIntField(
                    name=FieldName.DC_I_P_TOTAL,
                    address=144,
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=140,
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 2
