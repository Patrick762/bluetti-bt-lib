from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EP760(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField("b_soc_total", 102),
                StringField("d_inverter_type", 110),
                SerialNumberField("d_serial", 116),
                UIntField("pv_1_i_p", 1212),
                UIntField("pv_1_i_v", 1213),
                UIntField("pv_1_i_c", 1214),
                UIntField("pv_2_i_p", 1220),
                UIntField("pv_2_i_v", 1221),
                UIntField("pv_2_i_c", 1222),
                UIntField("g_i_f", 1300),
                UIntField("ac_o_f", 1500),
                UIntField("ac_1_o_p", 1510),
                UIntField("ac_1_o_v", 1511),
                UIntField("ac_1_o_c", 1512),
            ]
        )
