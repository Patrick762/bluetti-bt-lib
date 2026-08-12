from ..base_devices import BaseDeviceV2
from ..fields import FieldName, UIntField, DecimalField, SwapStringField, SerialNumberField, SignedDecimalField, AbsoluteSignedDecimalField


class CHARGER2(BaseDeviceV2):
    def __init__(self):
        super().__init__(
            [
                DecimalField(FieldName.DC_INPUT_VOLTAGE, 15531, 1),
                DecimalField(FieldName.DC_INPUT_CURRENT, 15532, 2),
                UIntField(FieldName.DC_INPUT_POWER, 15534),
                DecimalField(FieldName.PPS_OUTPUT_VOLTAGE, 15535, 1),
                AbsoluteSignedDecimalField(FieldName.PPS_OUTPUT_CURRENT, 15536, 2),
                AbsoluteSignedDecimalField(FieldName.PPS_OUTPUT_POWER, 15538, 0),
                DecimalField(FieldName.PS_BATTERY_VOLTAGE, 15543, 1),
                AbsoluteSignedDecimalField(FieldName.PS_BATTERY_IO_POWER, 15546, 0),
                UIntField(FieldName.PS_BATTERY_SOC, 15584),
                UIntField(FieldName.BATTERY_SOC, 15584),
                DecimalField(FieldName.BATTERY_VOLTAGE, 15539, 1),
                DecimalField(FieldName.BATTERY_CURRENT, 15540, 2),
                DecimalField(FieldName.BATTERY_IO_POWER, 15542, 0),
                SwapStringField(FieldName.DEVICE_TYPE, 15500, 6),
                SerialNumberField(FieldName.DEVICE_SN, 15506),
            ],
        )