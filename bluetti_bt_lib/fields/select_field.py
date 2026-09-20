from enum import Enum
from typing import Any, Type, TypeVar

from . import EnumField, FieldName


E = TypeVar("E", bound=Enum)


class SelectField(EnumField):
    def __init__(self, name: FieldName, address: int, e: Type[E]):
        super().__init__(name, address, 1)
        self.e = e

    def is_writeable(self):
        return True

    def allowed_write_type(self, value: Any) -> bool:
        return isinstance(value, self.e)
