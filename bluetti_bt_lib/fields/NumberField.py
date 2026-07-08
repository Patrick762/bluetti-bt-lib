from .UIntField import UIntField


class NumberField(UIntField):
    def is_writeable(self) -> bool:
        return True

    def allowed_write_type(self, value) -> bool:
        return isinstance(value, (int, float))
