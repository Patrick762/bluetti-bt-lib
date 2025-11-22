"""Device info helper."""

from ..devices import DEVICE_NAME_RE


def get_type_by_bt_name(bt_name: str):
    """Check bluetooth name and return type if supported."""

    match = DEVICE_NAME_RE.match(bt_name)
    if match is None:
        return None
    return match[1]
