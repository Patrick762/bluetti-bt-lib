from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class AC200PL(BluettiDevice):
    def __init__(self):
        super().__init__([
			UIntField("ac_1_o_v", 71),
			UIntField("ac_i_p_total", 37),
			UIntField("ac_o_f", 74),
			EnumField("ac_o_mode", 70),
			UIntField("ac_o_p_total", 38),
			BoolField("ac_o_switch", 3007),
			UIntField("b_soc_total", 43),
			EnumField("d_display_mode", 3061),
			StringField("d_inverter_type", 10),
			BoolField("d_power_off", 3060),
			SerialNumberField("d_serial", 17),
			UIntField("dc_i_p_total", 36),
			UIntField("dc_i_v", 86),
			UIntField("dc_o_p_total", 39),
			BoolField("dc_o_switch", 3008),
			UIntField("pv_1_i_c", 88),
			UIntField("pv_1_i_p", 87),
        ])
