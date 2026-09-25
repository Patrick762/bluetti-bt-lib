from .uint_field import UIntField


class TimeField(UIntField):
    """Returns a duration in seconds."""

    def __init__(self, name, address, multiplier = 360, min = None, max = None, **kwargs):
        super().__init__(name, address, multiplier, min, max, **kwargs)
