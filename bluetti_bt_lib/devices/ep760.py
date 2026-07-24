from ..base_devices import BaseDeviceV2
from ..fields import FieldName, UIntField, DecimalField, SwitchField

class EP760(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.PV_S1_POWER, 1212),
                DecimalField(FieldName.PV_S1_VOLTAGE, 1213, 1),
                DecimalField(FieldName.PV_S1_CURRENT, 1214, 1),
                UIntField(FieldName.PV_S2_POWER, 1220),
                DecimalField(FieldName.PV_S2_VOLTAGE, 1221, 1),
                DecimalField(FieldName.PV_S2_CURRENT, 1222, 1),
                # Reclassified from SM_P1 (smart meter) - confirmed against
                # live hardware to be PV String 3, not a smart meter channel.
                UIntField(FieldName.PV_S3_POWER, 1228),
                DecimalField(FieldName.PV_S3_VOLTAGE, 1229, 1),
                UIntField(FieldName.PV_S3_CURRENT, 1230, 1),
                DecimalField(FieldName.GRID_FREQUENCY, 1300, 1),
                UIntField(FieldName.GRID_P1_POWER, 1313),
                DecimalField(FieldName.GRID_P1_VOLTAGE, 1314, 1),
                DecimalField(FieldName.GRID_P1_CURRENT, 1315, 1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                UIntField(FieldName.AC_P1_POWER, 1510),
                DecimalField(FieldName.AC_P1_VOLTAGE, 1511, 1),
                DecimalField(FieldName.AC_P1_CURRENT, 1512, 1),
                SwitchField(FieldName.CTRL_AC, 2208),
                # Low/High SOC display - register matches EP600, EP2000, AC300,
                # AC500, EP500, and your old library's commented mapping.
                UIntField(FieldName.BATTERY_SOC_RANGE_START, 2022),
                UIntField(FieldName.BATTERY_SOC_RANGE_END, 2023),
                # --- Added: HA Energy dashboard totals (from old library) ---
                DecimalField(FieldName.DC_INPUT_POWER, 144,1),
                DecimalField(FieldName.TOTAL_LOAD_CONSUMPTION, 152, 1),
                DecimalField(FieldName.POWER_GENERATION, 154, 1),
                DecimalField(FieldName.TOTAL_GRID_CONSUMPTION, 156, 1),
                DecimalField(FieldName.TOTAL_GRID_FEED, 158, 1),
                SwitchField(FieldName.CTRL_WORKING_MODE, 2029),
                SwitchField(FieldName.CTRL_CHARGE_FROM_GRID, 2207),
           ],
        )
