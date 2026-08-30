from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class AC50B(BluettiDevice):
    def __init__(self):
        super().__init__([
			UIntField("b_soc_total", 102),
			UIntField("d_time_remaining", 104),
			StringField("d_inverter_type", 110),
			SerialNumberField("d_serial", 116),
			UIntField("dc_o_p_total", 140),
			UIntField("ac_o_p_total", 142),
			UIntField("ac_i_p_total", 146),
        ])
