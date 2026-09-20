from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class BaseDeviceV2(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
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
            ]
        )
