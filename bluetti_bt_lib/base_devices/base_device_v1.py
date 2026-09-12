from typing import List

from . import BluettiDevice
from ..fields import DeviceField
from ..fields import FieldName, StringField, SerialNumberField
from ..registers import ReadableRegisters, WriteableRegister


class BaseDeviceV1(BluettiDevice):
    def __init__(
        self,
        additional_fields: List[DeviceField] = [],
        pack_fields: List[DeviceField] = [],
        max_packs: int = 0,
    ):
        super().__init__(
            [
                StringField(FieldName.DEVICE_TYPE, 10, 6),
                SerialNumberField(FieldName.DEVICE_SN, 17),
            ]
            + additional_fields,
            pack_fields,
            max_packs,
        )

    def get_full_registers_range(self) -> List[ReadableRegisters]:
        return [ReadableRegisters(i, 10) for i in range(0, 8000, 10)]

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

    def get_pack_selector(self, pack: int) -> WriteableRegister:
        return WriteableRegister(3006, pack)
