from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class BaseDeviceV1(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.AC_I_P_TOTAL, 37),
                UIntField(FieldName.AC_O_P_TOTAL, 38),
                UIntField(FieldName.B_SOC_TOTAL, 43),
                StringField(FieldName.D_INVERTER_TYPE, 10),
                SerialNumberField(FieldName.D_SERIAL, 17),
                UIntField(FieldName.DC_I_P_TOTAL, 36),
                UIntField(FieldName.DC_O_P_TOTAL, 39),
            ]
        )
