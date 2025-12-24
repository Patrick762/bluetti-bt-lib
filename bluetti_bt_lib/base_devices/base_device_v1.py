from typing import List

from . import BluettiDevice
from ..fields import DeviceField
from ..fields import FieldName, StringField, UIntField, SerialNumberField
from ..registers import ReadableRegisters


class BaseDeviceV1(BluettiDevice):
    def __init__(self, additional_fields: List[DeviceField] = []):
        super().__init__(
            [
                StringField(FieldName.DEVICE_TYPE, 10, 6),
                SerialNumberField(FieldName.DEVICE_SN, 17),
                UIntField(FieldName.BATTERY_SOC, 43, min=0, max=100),
                UIntField(FieldName.DC_INPUT_POWER, 36),
                UIntField(FieldName.AC_INPUT_POWER, 37),
                UIntField(FieldName.AC_OUTPUT_POWER, 38),
                UIntField(FieldName.DC_OUTPUT_POWER, 39),
            ]
            + additional_fields,
        )

    def get_full_registers_range(self) -> List[ReadableRegisters]:
        return [ReadableRegisters(i, 50) for i in range(1, 8000, 50)]

    def get_device_type_registers(self) -> List[ReadableRegisters]:
        return [
            ReadableRegisters(10, 6),
        ]

    def get_device_sn_registers(self) -> List[ReadableRegisters]:
        return [
            ReadableRegisters(17, 4),
        ]

    def get_iot_version(self) -> int:
        return 1
