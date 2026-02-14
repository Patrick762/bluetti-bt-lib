from enum import Enum, unique


@unique
class LedMode(Enum):
    """Writable LED control mode (e.g. EB3A)."""
    LOW = 1
    HIGH = 2
    SOS = 3
    OFF = 4


@unique
class LedPanelState(Enum):
    """Read-only LED panel state at register 2007. Used by AC60, EL10, and similar devices."""
    OFF = 0
    NORMAL = 1
    BRIGHT = 2
    BLINKING = 3
