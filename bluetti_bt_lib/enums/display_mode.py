from enum import Enum, unique


@unique
class DisplayMode(Enum):
    SEC30 = 2
    MIN1 = 3
    MIN5 = 4
    NEVER = 5
