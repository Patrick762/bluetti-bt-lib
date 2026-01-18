from ..base_devices import BaseDeviceV2
from ..fields import (
    UIntField,
    DecimalField,
    BoolField,
    SwapStringField,
    FieldName,
)


class EP2000(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.PV_S1_POWER, 1212),
                DecimalField(FieldName.PV_S1_VOLTAGE, 1213, 1),
                DecimalField(FieldName.PV_S1_CURRENT, 1214, 1),
                UIntField(FieldName.PV_S2_POWER, 1220),
                DecimalField(FieldName.PV_S2_VOLTAGE, 1221, 1),
                DecimalField(FieldName.PV_S2_CURRENT, 1222, 1),
                DecimalField(FieldName.GRID_FREQUENCY, 1300, 1),
                DecimalField(FieldName.GRID_P1_VOLTAGE, 1314, 1),
                DecimalField(FieldName.GRID_P2_VOLTAGE, 1320, 1),
                DecimalField(FieldName.GRID_P3_VOLTAGE, 1326, 1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                DecimalField(FieldName.AC_P1_VOLTAGE, 1511, 1),
                DecimalField(FieldName.AC_P2_VOLTAGE, 1518, 1),
                DecimalField(FieldName.AC_P3_VOLTAGE, 1525, 1),
                BoolField(FieldName.CTRL_AC, 2011),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023),
                BoolField(FieldName.CTRL_GENERATOR, 2246),
                DecimalField(FieldName.GRID_VOLT_MIN_VAL, 2435, 1),
                DecimalField(FieldName.GRID_VOLT_MAX_VAL, 2436, 1),
                DecimalField(FieldName.GRID_FREQ_MIN_VALUE, 2437, 2),
                DecimalField(FieldName.GRID_FREQ_MAX_VALUE, 2438, 2),
                SwapStringField(FieldName.WIFI_NAME, 12002, 16),
            ],
        )
