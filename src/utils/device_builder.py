"""Device builder helper."""

from ..base_devices import BluettiDevice

from ..devices import DEVICES, DEVICE_NAME_RE


def build_device(name: str) -> BluettiDevice | None:
    devMatch = DEVICE_NAME_RE.match(name)

    if devMatch is None:
        return None

    devType = devMatch[1]

    if devType is None:
        return None

    Station = DEVICES.get(devType)

    if Station is None:
        return None

    return Station()
