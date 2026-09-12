from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class EL30V2(BluettiDevice):
    def __init__(self):
        super().__init__([
			EnumField("ac_eco_mode", 2018),
			BoolField("ac_eco_switch", 2017),
			UIntField("ac_1_i_v", 1314),
			UIntField("ac_i_p_total", 146),
			UIntField("ac_o_p_total", 142),
			BoolField("ac_o_switch", 2011),
			BoolField("ac_power_lifting_switch", 2021),
			UIntField("b_soc_total", 102),
			EnumField("d_charging_mode", 2020),
			SwapStringField("d_inverter_type", 110),
			SerialNumberField("d_serial", 116),
			TimeField("d_time_remaining", 104),
			EnumField("dc_eco_mode", 2015),
			BoolField("dc_eco_switch", 2014),
			UIntField("dc_i_p_total", 144),
			UIntField("dc_o_p_total", 140),
			BoolField("dc_o_switch", 2012),
        ])
