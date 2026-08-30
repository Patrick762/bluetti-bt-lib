from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class AC60(BluettiDevice):
    def __init__(self):
        super().__init__([
			UIntField("b_soc_total", 102),
			StringField("d_inverter_type", 110),
			SerialNumberField("d_serial", 116),
			UIntField("dc_o_p_total", 140),
			UIntField("ac_o_p_total", 142),
			UIntField("dc_i_p_total", 144),
			UIntField("ac_i_p_total", 146),
			UIntField("ac_i_v", 1314),
			BoolField("ac_o_switch", 2011),
			BoolField("dc_o_switch", 2012),
			BoolField("ac_power_lifting_switch", 2021),
        ])
