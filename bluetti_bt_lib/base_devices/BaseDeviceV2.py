from typing import List

from . import BluettiDevice
from ..fields import DeviceField
from ..fields import FieldName, SwapStringField, UIntField
from ..registers import ReadableRegisters


class BaseDeviceV2(BluettiDevice):
    def __init__(self, additional_fields: List[DeviceField] = []):
        super().__init__(
            [
                SwapStringField(FieldName.DEVICE_TYPE, 110, 6),
                UIntField(FieldName.BATTERY_SOC, 102),
            ]
            + additional_fields,
        )

    def get_device_type_registers(self) -> List[ReadableRegisters]:
        return [
            ReadableRegisters(110, 6),
        ]

    def get_iot_version(self) -> int:
        return 2
