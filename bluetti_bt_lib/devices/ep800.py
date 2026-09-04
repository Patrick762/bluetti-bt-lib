from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EP800(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField("b_soc_total", 102),
                StringField("d_inverter_type", 110),
                SerialNumberField("d_serial", 116),
            ]
        )
