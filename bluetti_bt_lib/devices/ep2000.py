from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class EP2000(BluettiDevice):
    def __init__(self):
        super().__init__([
			UIntField("ac_1_o_v", 1511),
			UIntField("ac_2_o_v", 1518),
			UIntField("ac_3_o_v", 1525),
			UIntField("ac_i_f", 1300),
			UIntField("ac_1_i_v", 1314),
			UIntField("ac_2_i_v", 1320),
			UIntField("ac_3_i_v", 1326),
			UIntField("ac_o_f", 1500),
			BoolField("ac_o_switch", 2011),
			UIntField("b_soc_high", 2023),
			UIntField("b_soc_low", 2022),
			UIntField("b_soc_total", 102),
			SwapStringField("d_inverter_type", 110),
			SerialNumberField("d_serial", 116),
			UIntField("g_i_f", 1300),
			UIntField("pv_1_i_c", 1214),
			UIntField("pv_1_i_p", 1212),
			UIntField("pv_1_i_v", 1213),
			UIntField("pv_2_i_c", 1222),
			UIntField("pv_2_i_p", 1220),
			UIntField("pv_2_i_v", 1221),
        ])
