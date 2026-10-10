from enum import Enum, unique


@unique
class UpsModeV2(Enum):
    CUSTOMIZED = 1
    PV_PRIORITY = 2
    STANDARD = 4
    TIME_CONTROL = 5
