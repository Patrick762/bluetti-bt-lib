from . import DeviceField, FieldName


class StringField(DeviceField):
    def __init__(self, name: FieldName, address: int, size: int, **kwargs):
        super().__init__(name, address, size, **kwargs)

    def parse(self, data: bytes) -> str:
        return data.rstrip(b"\0").decode("ascii", errors="ignore")
