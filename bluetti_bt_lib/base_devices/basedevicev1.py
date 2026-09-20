from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class BaseDeviceV1(BluettiDevice):
    def __init__(self):
        super().__init__(
            [
                UIntField(
                    name=FieldName.AC_I_P_TOTAL,
                    address=37,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.AC_O_P_TOTAL,
                    address=38,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.B_SOC_TOTAL,
                    address=43,
                    unit="%",
                    sensor="battery",
                    state_type="measurement",
                ),
                StringField(
                    name=FieldName.D_INVERTER_TYPE,
                    address=10,
                    size=6,
                ),
                SerialNumberField(
                    name=FieldName.D_SERIAL,
                    address=17,
                ),
                UIntField(
                    name=FieldName.DC_I_P_TOTAL,
                    address=36,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
                UIntField(
                    name=FieldName.DC_O_P_TOTAL,
                    address=39,
                    unit="W",
                    sensor="power",
                    state_type="measurement",
                ),
            ]
        )

    def get_iot_version(self) -> int:
        return 1
