import re

from .ac70 import AC70
from .ac180 import AC180
from .eb3a import EB3A
from .handsfree1 import Handsfree1

# Add new device classes here
DEVICES = {
    "AC70": AC70,
    "AC180": AC180,
    "EB3A": EB3A,
    "Handsfree 1": Handsfree1,
}

# Prefixes of all currently supported devices
DEVICE_NAME_RE = re.compile(
    r"^(AC2A|AC60|AC60P|AC70|AC70P|AC180|AC180P|AC200L|AC200M|AC200PL|AC300|AC500|EB3A|EP500|EP500P|EP600|EP760|EP800|Handsfree\ 1)(\d+)$"
)
