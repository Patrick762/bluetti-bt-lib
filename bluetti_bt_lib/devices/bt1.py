from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class BT1(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField("ac_i_p_total", 37),
                UIntField("ac_o_p_total", 38),
                UIntField("b_soc_total", 43),
                StringField("d_inverter_type", 10),
                SerialNumberField("d_serial", 17),
                UIntField("dc_i_p_total", 36),
                UIntField("dc_o_p_total", 39),
            ]
        )
