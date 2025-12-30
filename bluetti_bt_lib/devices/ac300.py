from ..base_devices import BaseDeviceV1
from ..fields import (
    FieldName,
    EnumField,
    DecimalField,
    UIntField,
    SelectField,
    BoolField,
    DecimalArrayField,
    SwitchField,
    VersionField,
)
from ..enums import OutputMode, UpsMode, SplitPhaseMode


class AC300(BaseDeviceV1):
    def __init__(self):
        super().__init__(
            [
                VersionField(FieldName.VER_ARM, 23),
                VersionField(FieldName.VER_DSP, 25),
                DecimalField(FieldName.POWER_GENERATION, 43, 1),
                EnumField(FieldName.AC_OUTPUT_MODE, 70, OutputMode),
                DecimalField(FieldName.INTERNAL_AC_VOLTAGE, 71, 1),
                DecimalField(FieldName.INTERNAL_AC_FREQUENCY, 74, 2),
                DecimalField(FieldName.AC_INPUT_VOLTAGE, 77, 1),
                DecimalField(FieldName.AC_INPUT_FREQUENCY, 80, 2),
                DecimalField(FieldName.PV_S1_VOLTAGE, 86, 1),
                DecimalField(FieldName.PV_S1_POWER, 87, 1, 10),
                DecimalField(FieldName.PV_S1_CURRENT, 88, 2, 10),
                SelectField(FieldName.CTRL_UPS_MODE, 3001, UpsMode),
                BoolField(FieldName.CTRL_SPLIT_PHASE, 3004),
                EnumField(FieldName.CTRL_SPLIT_PHASE_MODE, 3005, SplitPhaseMode),
                SwitchField(FieldName.CTRL_AC, 3007),
                SwitchField(FieldName.CTRL_DC, 3008),
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 3015),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 3016),
                # SelectField(FieldName.CTRL_DISPLAY_TIMEOUT, 3061, DisplayMode),
            ],
            [
                UIntField(FieldName.PACK_SELECTED, 96),
                DecimalField(FieldName.PACK_VOLTAGE, 98, 2),
                UIntField(FieldName.PACK_BATTERY_SOC, 99),
                DecimalArrayField(FieldName.PACK_CELL_VOLTAGES, 105, 16, 2),
                # VersionField(FieldName.VER_BMS, 201),
            ],
            max_packs=4,
        )
