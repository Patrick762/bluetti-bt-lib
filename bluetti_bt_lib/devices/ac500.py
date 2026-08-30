from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class AC500(BluettiDevice):
    def __init__(self):
        super().__init__([
			StringField("d_inverter_type", 10),
			SerialNumberField("d_serial", 17),
			UIntField("dc_i_p_total", 36),
			UIntField("ac_i_p_total", 37),
			UIntField("ac_o_p_total", 38),
			UIntField("dc_o_p_total", 39),
			UIntField("b_soc_total", 43),
			EnumField("ac_o_mode", 70),
			UIntField("ac_i_v", 77),
			UIntField("pv_1_i_v", 86),
			UIntField("pv_1_i_p", 87),
			UIntField("pv_1_i_c", 88),
			EnumField("ac_ups_mode", 3001),
			BoolField("d_split_phase_switch", 3004),
			EnumField("d_split_phase_mode", 3005),
			BoolField("ac_o_switch", 3007),
			BoolField("dc_o_switch", 3008),
			UIntField("b_soc_low", 3015),
			UIntField("b_soc_high", 3016),
			EnumField("d_display_mode", 3061),
        ])
