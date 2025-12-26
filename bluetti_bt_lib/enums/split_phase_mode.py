from enum import Enum, unique


@unique
class SplitPhaseMode(Enum):
    SLAVE = 0
    MASTER = 1
