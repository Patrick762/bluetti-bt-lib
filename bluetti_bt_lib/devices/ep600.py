from ..base_devices import BaseDeviceV2
from ..fields import FieldName, UIntField, DecimalField, IntField


class EP600(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                UIntField(FieldName.PV_S1_POWER, 1212),
                DecimalField(FieldName.PV_S1_VOLTAGE, 1213, 1),
                DecimalField(FieldName.PV_S1_CURRENT, 1214, 1),
                UIntField(FieldName.PV_S2_POWER, 1220),
                DecimalField(FieldName.PV_S2_VOLTAGE, 1221, 1),
                DecimalField(FieldName.PV_S2_CURRENT, 1222, 1),
                UIntField(FieldName.SM_P1_POWER, 1228),
                DecimalField(FieldName.SM_P1_VOLTAGE, 1229, 1),
                UIntField(FieldName.SM_P1_CURRENT, 1230, 1),
                UIntField(FieldName.SM_P2_POWER, 1236),
                DecimalField(FieldName.SM_P2_VOLTAGE, 1237, 1),
                UIntField(FieldName.SM_P2_CURRENT, 1238, 1),
                UIntField(FieldName.SM_P3_POWER, 1244),
                DecimalField(FieldName.SM_P3_VOLTAGE, 1245, 1),
                UIntField(FieldName.SM_P3_CURRENT, 1246, 1),
                DecimalField(FieldName.GRID_FREQUENCY, 1300, 1),
                UIntField(FieldName.GRID_P1_POWER, 1313),
                DecimalField(FieldName.GRID_P1_VOLTAGE, 1314, 1),
                DecimalField(FieldName.GRID_P1_CURRENT, 1315, 1),
                UIntField(FieldName.GRID_P2_POWER, 1319),
                DecimalField(FieldName.GRID_P2_VOLTAGE, 1320, 1),
                DecimalField(FieldName.GRID_P2_CURRENT, 1321, 1),
                UIntField(FieldName.GRID_P3_POWER, 1325),
                DecimalField(FieldName.GRID_P3_VOLTAGE, 1326, 1),
                DecimalField(FieldName.GRID_P3_CURRENT, 1327, 1),
                DecimalField(FieldName.AC_OUTPUT_FREQUENCY, 1500, 1),
                IntField(FieldName.AC_P1_POWER, 1510),
                DecimalField(FieldName.AC_P1_VOLTAGE, 1511, 1),
                DecimalField(FieldName.AC_P1_CURRENT, 1512, 1),
                IntField(FieldName.AC_P2_POWER, 1517),
                DecimalField(FieldName.AC_P2_VOLTAGE, 1518, 1),
                DecimalField(FieldName.AC_P2_CURRENT, 1519, 1),
                IntField(FieldName.AC_P3_POWER, 1524),
                DecimalField(FieldName.AC_P3_VOLTAGE, 1525, 1),
                DecimalField(FieldName.AC_P3_CURRENT, 1526, 1),
            ],
        )
