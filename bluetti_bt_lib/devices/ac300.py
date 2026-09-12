from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class AC300(BluettiDevice):
    def __init__(self):
        super().__init__([
			UIntField("ac_1_o_v", 71),
			UIntField("ac_i_f", 80),
			UIntField("ac_1_i_v", 77),
			UIntField("ac_i_p_total", 37),
			UIntField("ac_o_f", 74),
			EnumField("ac_o_mode", 70),
			UIntField("ac_o_p_total", 38),
			BoolField("ac_o_switch", 3007),
			EnumField("ac_ups_mode", 3001),
			UIntField("b_soc_high", 3016),
			UIntField("b_soc_low", 3015),
			UIntField("b_soc_total", 43),
			StringField("d_inverter_type", 10),
			SerialNumberField("d_serial", 17),
			BoolField("d_split_phase_switch", 3004),
			EnumField("d_split_phase_mode", 3005),
			VersionField("d_ver_arm", 23),
			VersionField("d_ver_dsp", 25),
			UIntField("dc_i_p_total", 36),
			UIntField("dc_o_p_total", 39),
			BoolField("dc_o_switch", 3008),
			UIntField("pv_1_i_c", 88),
			UIntField("pv_1_i_p", 87),
			UIntField("pv_1_i_v", 86),
        ])
