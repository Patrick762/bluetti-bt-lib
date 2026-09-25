from ..base_devices import BluettiDevice
from ..enums import *
from ..fields import *
from ..registers import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EP800(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
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
            ]
        )

    def get_iot_version(self) -> int:
        return 2
