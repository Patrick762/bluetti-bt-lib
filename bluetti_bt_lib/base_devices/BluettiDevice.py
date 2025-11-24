from typing import Any, List

from ..registers import ReadableRegisters, WriteableRegister
from ..fields import DeviceField, EnumField, BoolField, SwitchField, SelectField


class BluettiDevice:
    def __init__(self, fields: List[DeviceField]):
        self.fields = fields

    def addFields(self, fields: List[DeviceField]):
        for f in fields:
            self.fields.append(f)

    def get_polling_registers(self) -> List[ReadableRegisters]:
        result = []

        # TODO Optimize this to reduce amount of registers to separately request

        for f in self.fields:
            result.append(ReadableRegisters(f.address, f.size))

        return result

    def get_device_type_registers(self) -> List[ReadableRegisters]:
        raise NotImplementedError

    def get_iot_version(self) -> int:
        raise NotImplementedError

    def parse(self, starting_address: int, data: bytes) -> dict:
        # Offsets and size are counted in 2 byte chunks, so for the range we
        # need to divide the byte size by 2
        data_size = int(len(data) / 2)

        # Filter out fields not in range
        r = range(starting_address, starting_address + data_size)
        fields = [
            f for f in self.fields if f.address in r and f.address + f.size - 1 in r
        ]

        # Parse fields
        parsed = {}
        for f in fields:
            data_start = 2 * (f.address - starting_address)
            field_data = data[data_start : data_start + 2 * f.size]
            parsed[f.name] = f.parse(field_data)

        return parsed

    def build_write_command(self, name: str, value: Any) -> WriteableRegister:
        matches = [f for f in self.fields if f.name == name]
        field = next(f for f in matches if f.is_writeable)

        # Convert value to an integer
        if isinstance(field, EnumField):
            value = field.enum[value].value
        elif isinstance(field, BoolField):
            value = 1 if value else 0

        return WriteableRegister(field.address, value)

    def get_bool_fields(self):
        return [f for f in self.fields if isinstance(f, BoolField)]

    def get_switch_fields(self):
        return [f for f in self.fields if isinstance(f, SwitchField)]

    def get_select_fields(self):
        return [f for f in self.fields if isinstance(f, SelectField)]

    def get_sensor_fields(self):
        return [
            f
            for f in self.fields
            if not isinstance(f, BoolField)
            and not isinstance(f, SwitchField)
            and not isinstance(f, SelectField)
        ]
