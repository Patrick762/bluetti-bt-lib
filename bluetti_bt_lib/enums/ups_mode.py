from enum import Enum, unique


@unique
class UpsMode(Enum):
    CUSTOMIZED = 1
    PV_PRIORITY = 2
    STANDARD = 3
    TIME_CONTROL = 4
