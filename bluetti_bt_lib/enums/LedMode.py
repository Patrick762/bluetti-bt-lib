from enum import Enum, unique


@unique
class LedMode(Enum):
    LOW = 1
    HIGH = 2
    SOS = 3
    OFF = 4
