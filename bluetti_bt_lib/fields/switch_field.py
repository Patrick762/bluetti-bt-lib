from typing import Any

from . import BoolField


class SwitchField(BoolField):
    def is_writeable(self) -> bool:
        return True

    def allowed_write_type(self, value: Any) -> bool:
        return isinstance(value, bool)
