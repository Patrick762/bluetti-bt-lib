from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class Handsfree2(BluettiDevice):
    def __init__(self):
        super().__init__([
			UIntField("ac_1_o_v", 1511),
			UIntField("ac_i_f", 1300),
			UIntField("ac_1_i_c", 1315),
			UIntField("ac_1_i_v", 1314),
			UIntField("ac_i_p_total", 146),
			UIntField("ac_o_f", 1500),
			UIntField("ac_o_p_total", 142),
			BoolField("ac_o_switch", 2011),
			UIntField("b_soc_total", 102),
			SwapStringField("d_inverter_type", 110),
			SerialNumberField("d_serial", 116),
			TimeField("d_time_remaining", 104),
			UIntField("dc_i_c", 1214),
			UIntField("dc_i_p_total", 144),
			UIntField("dc_i_v", 1213),
			UIntField("dc_o_p_total", 140),
			BoolField("dc_o_switch", 2012),
			UIntField("g_i_f", 1300),
        ])
