"""EL10 LED torch modes (per readall analysis: off, cold, warm, sos)."""

from enum import Enum, unique


@unique
class EL10LedMode(Enum):
    OFF = 0
    COLD = 1
    WARM = 2
    SOS = 3
