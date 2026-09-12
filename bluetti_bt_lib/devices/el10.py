from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class EL10(BluettiDevice):
    def __init__(self):
        super().__init__([
			UIntField("ac_1_o_v", 1511),
			EnumField("ac_eco_mode", 2018),
			BoolField("ac_eco_switch", 2017),
			UIntField("ac_1_i_c", 1315),
			UIntField("ac_1_i_v", 1314),
			UIntField("ac_i_p_total", 146),
			UIntField("ac_o_p_total", 142),
			BoolField("ac_o_switch", 2011),
			BoolField("ac_power_lifting_switch", 2021),
			UIntField("b_soc_total", 102),
			VersionField("b_ver_bms", 6175),
			EnumField("d_charging_mode", 2020),
			EnumField("d_display_mode", 2067),
			SwapStringField("d_inverter_type", 110),
			SerialNumberField("d_serial", 116),
			TimeField("d_time_remaining", 104),
			EnumField("dc_eco_mode", 2015),
			BoolField("dc_eco_switch", 2014),
			UIntField("dc_i_p_total", 144),
			UIntField("dc_o_p_total", 140),
			BoolField("dc_o_switch", 2012),
        ])
