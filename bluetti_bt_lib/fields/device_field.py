from typing import Any

from . import FieldName


class DeviceField:
    def __init__(
        self,
        name: FieldName,
        address: int,
        size: int,
        unit: str | None = None,
        sensor: str | None = None,
        state_type: str | None = None,
    ):
        self.name = name.value
        self.address = address
        self.size = size
        self.unit = unit
        self.sensor = sensor
        self.state_type = state_type

    def parse(self, data: bytes) -> Any:
        raise NotImplementedError

    def is_writeable(self) -> bool:
        return False

    def allowed_write_type(self, value: Any) -> bool:
        return False

    def in_range(self, value: Any) -> bool:
        return True
