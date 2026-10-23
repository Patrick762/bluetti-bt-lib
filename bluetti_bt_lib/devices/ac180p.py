from decimal import Decimal

from ..base_devices import BaseDeviceV2
from ..enums import ChargingMode
from ..fields import FieldName, UIntField, SwitchField, SelectField, DecimalField


class AC180P(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.DC_OUTPUT_POWER, 140),
                UIntField(FieldName.AC_OUTPUT_POWER, 142),
                UIntField(FieldName.DC_INPUT_POWER, 144),
                UIntField(FieldName.AC_INPUT_POWER, 146),
                DecimalField(FieldName.DC_INPUT_VOLTAGE, 1213, 1),
                DecimalField(FieldName.DC_INPUT_CURRENT, 1214, 1),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 1314, 1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                DecimalField(FieldName.AC_OUTPUT_VOLTAGE, 1511, 1),
                SwitchField(FieldName.CTRL_AC, 2011),
                SwitchField(FieldName.CTRL_DC, 2012),
                SelectField(FieldName.CTRL_CHARGING_MODE, 2020, ChargingMode),
                SwitchField(FieldName.CTRL_POWER_LIFTING, 2021),
                # TODO SoC limits: both registers read 0 on a unit without limits
                # set in the app (IoT protocol 2004). Enable them once a read
                # after setting limits in the app confirms the mapping.
                # UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022, min=0, max=100),
                # UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023, min=0, max=100),
                UIntField(FieldName.BATTERY_SOH, 6006, min=1, max=100),
                # Raw value is offset by 40, a raw 0 means no sensor
                DecimalField(
                    FieldName.BATTERY_TEMPERATURE,
                    6007,
                    0,
                    offset=-40,
                    min=Decimal(-39),
                    max=Decimal(100),
                ),
            ],
        )
