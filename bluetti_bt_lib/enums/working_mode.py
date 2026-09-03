from enum import Enum, unique


@unique
class WorkingMode(Enum):
    CUSTOM = 1
    SELF_CONSUMPTION = 2
    BACKUP = 4
    TIME_OF_USE = 5
