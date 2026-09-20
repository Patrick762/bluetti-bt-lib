from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class BaseDeviceV1(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(
                    FieldName.AC_I_P_TOTAL,
                    37,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    FieldName.AC_O_P_TOTAL,
                    38,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    FieldName.B_SOC_TOTAL,
                    43,
                    unit="%",
                    sensor="battery",
                    state_type="measurement",
                ),
                StringField(
                    FieldName.D_INVERTER_TYPE,
                    10,
                ),
                SerialNumberField(
                    FieldName.D_SERIAL,
                    17,
                ),
                UIntField(
                    FieldName.DC_I_P_TOTAL,
                    36,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    FieldName.DC_O_P_TOTAL,
                    39,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
            ]
        )
