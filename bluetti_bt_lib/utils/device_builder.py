"""Device builder helper."""

from ..base_devices import BluettiDevice

from ..devices import DEVICES


def build_device(name: str) -> BluettiDevice | None:
    Station = DEVICES.get(name)

    if Station is None:
        return None

    return Station()
