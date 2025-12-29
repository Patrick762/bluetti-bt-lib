from typing import Any, List

from ..registers import ReadableRegisters, WriteableRegister
from ..fields import DeviceField, BoolField, SwitchField, SelectField


class BluettiDevice:
    def __init__(
        self,
        fields: List[DeviceField],
        pack_fields: List[DeviceField] = [],
        max_packs: int = 0,
    ):
        self.fields = fields
        self.pack_fields = pack_fields
        self.max_packs = max_packs

        self.fields.sort(key=lambda f: f.address)
        self.pack_fields.sort(key=lambda f: f.address)

        self.polling_registers: List[ReadableRegisters] = []
        self.pack_polling_registers: List[ReadableRegisters] = []

        for f in self.fields:
            group = ReadableRegisters(f.address, f.size)
            self.polling_registers.append(group)

        # Check if we even have battery pack fields defined
        if len(self.pack_fields) == 0 or max_packs == 0:
            return

        # Optimize amount of registers to separately request
        for f in self.pack_fields:
            group = ReadableRegisters(f.address, f.size)
            self.pack_polling_registers.append(group)

    def get_polling_registers(self) -> List[ReadableRegisters]:
        """Returns all registers required to poll device fields"""
        return self.polling_registers

    def get_pack_polling_registers(self) -> List[ReadableRegisters]:
        """Returns all registers required to poll device battery pack fields"""
        return self.pack_polling_registers

    def get_full_registers_range(self) -> List[ReadableRegisters]:
        """Returns all registers which are tested with the readall command"""
        raise NotImplementedError

    def get_device_type_registers(self) -> List[ReadableRegisters]:
        """Returns the register storing the type of the device"""
        raise NotImplementedError

    def get_device_sn_registers(self) -> List[ReadableRegisters]:
        """Returns the register storing the serial number of the device"""
        raise NotImplementedError

    def get_iot_version(self) -> int:
        """Get the IoT protocol version of the device"""
        raise NotImplementedError

    def get_pack_selector(self, pack: int) -> WriteableRegister:
        """Returns the register to request a specific battery pack"""
        raise NotImplementedError

    def parse(
        self, starting_address: int, data: bytes, pack_num: int | None = None
    ) -> dict:
        """Parse data"""

        # Offsets and size are counted in 2 byte chunks, so for the range we
        # need to divide the byte size by 2
        data_size = int(len(data) / 2)

        # Filter out fields not in range
        r = range(starting_address, starting_address + data_size)
        fields = [
            f
            for f in (self.fields + self.pack_fields)
            if f.address in r and f.address + f.size - 1 in r
        ]

        # Parse fields
        parsed = {}
        for f in fields:
            data_start = 2 * (f.address - starting_address)
            field_data = data[data_start : data_start + 2 * f.size]
            value = f.parse(field_data)
            if not f.in_range(value):
                continue
            if pack_num is not None and f in self.pack_fields:
                parsed[f"pack_{str(pack_num)}_{f.name}"] = value
            else:
                parsed[f.name] = value

        return parsed

    def build_write_command(self, name: str, value: Any) -> WriteableRegister | None:
        """Build a command to write values to the device"""

        matches = [f for f in self.fields if f.name == name]
        fields = [f for f in matches if f.is_writeable()]

        if len(fields) == 0:
            return None

        field = next(iter(fields))

        # Convert value to an integer
        if isinstance(field, SelectField):
            value = field.e[value].value
        elif isinstance(field, SwitchField):
            value = 1 if value else 0

        return WriteableRegister(field.address, value)

    def get_bool_fields(self):
        """Returns all bool fields for this device"""
        return [
            f
            for f in self.fields
            if isinstance(f, BoolField) and not isinstance(f, SwitchField)
        ]

    def get_switch_fields(self):
        """Returns all switch fields for this device"""
        return [f for f in self.fields if isinstance(f, SwitchField)]

    def get_select_fields(self):
        """Returns all select fields for this device"""
        return [f for f in self.fields if isinstance(f, SelectField)]

    def get_sensor_fields(self):
        """Returns all sensor fields for this device"""
        return [
            f
            for f in self.fields
            if not isinstance(f, BoolField)
            and not isinstance(f, SwitchField)
            and not isinstance(f, SelectField)
        ]
