from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class AC200M(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                StringField("d_inverter_type", 10),
                SerialNumberField("d_serial", 17),
                UIntField("dc_i_p_total", 36),
                UIntField("ac_i_p_total", 37),
                UIntField("ac_o_p_total", 38),
                UIntField("dc_o_p_total", 39),
                UIntField("b_soc_total", 43),
                EnumField("ac_o_mode", 70),
                BoolField("ac_o_switch", 3007),
                BoolField("d_power_off", 3060),
                EnumField("d_display_mode", 3061),
            ]
        )
