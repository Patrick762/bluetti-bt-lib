from typing import List

from . import BluettiDevice
from ..fields import DeviceField
from ..fields import FieldName, SwapStringField, UIntField, SerialNumberField
from ..registers import ReadableRegisters


class BaseDeviceV2(BluettiDevice):
    def __init__(self, additional_fields: List[DeviceField] = []):
        super().__init__(
            [
                SwapStringField(FieldName.DEVICE_TYPE, 110, 6),
                SerialNumberField(FieldName.DEVICE_SN, 116),
                UIntField(FieldName.BATTERY_SOC, 102),
            ]
            + additional_fields,
        )

    def get_device_type_registers(self) -> List[ReadableRegisters]:
        return [
            ReadableRegisters(110, 6),
        ]

    def get_device_sn_registers(self) -> List[ReadableRegisters]:
        return [
            ReadableRegisters(116, 4),
        ]

    def get_iot_version(self) -> int:
        return 2
