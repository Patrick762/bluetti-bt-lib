from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class EB3A(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                StringField("d_inverter_type", 10),
                SerialNumberField("d_serial", 17),
                VersionField("d_ver_arm", 23),
                VersionField("d_ver_dsp", 25),
                UIntField("dc_i_p_total", 36),
                UIntField("ac_i_p_total", 37),
                UIntField("ac_o_p_total", 38),
                UIntField("dc_o_p_total", 39),
                UIntField("b_soc_total", 43),
                UIntField("ac_i_v", 77),
                UIntField("dc_i_v", 86),
                BoolField("ac_o_switch", 3007),
                BoolField("dc_o_switch", 3008),
                EnumField("d_led_mode", 3034),
                BoolField("d_power_off", 3060),
                BoolField("ac_eco_switch", 3063),
                EnumField("ac_eco_mode", 3064),
                EnumField("d_charging_mode", 3065),
                BoolField("ac_power_lifting_switch", 3066),
            ]
        )
