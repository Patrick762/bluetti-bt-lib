from enum import Enum
from typing import Any

from .field_name import FieldName


class DeviceField:
    def __init__(
        self,
        name: FieldName,
        address: int,
        size: int,
    ) -> None:
        self.name = name.value
        self.address = address
        self.size = size

    def parse(self, data: bytes) -> bool | int | float | Enum | str | None:
        raise NotImplementedError

    def is_writeable(self) -> bool:
        return False

    def allowed_write_type(self, value: Any) -> bool:
        return False

    def in_range(self, value: Any) -> bool:
        return True
