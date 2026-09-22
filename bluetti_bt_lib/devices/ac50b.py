from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC50B(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
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
                TimeField(
                    name=FieldName.D_TIME_REMAINING,
                    address=104,
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=140,
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 2
