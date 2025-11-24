import re

from .ac2a import AC2A
from .ac60 import AC60
from .ac60p import AC60P
from .ac70 import AC70
from .ac70p import AC70P
from .ac180 import AC180
from .ac180p import AC180P
from .ac200l import AC200L
from .ac200m import AC200M
from .ac200pl import AC200PL
from .ac300 import AC300
from .ac500 import AC500
from .eb3a import EB3A
from .ep500 import EP500
from .ep500p import EP500P
from .ep600 import EP600
from .ep800 import EP800
from .handsfree1 import Handsfree1

# Add new device classes here
DEVICES = {
    "AC2A": AC2A,
    "AC60": AC60,
    "AC60P": AC60P,
    "AC70": AC70,
    "AC70P": AC70P,
    "AC180": AC180,
    "AC180P": AC180P,
    "AC200L": AC200L,
    "AC200M": AC200M,
    "AC200PL": AC200PL,
    "AC300": AC300,
    "AC500": AC500,
    "EB3A": EB3A,
    "EP500": EP500,
    "EP500P": EP500P,
    "EP600": EP600,
    "EP800": EP800,
    "Handsfree 1": Handsfree1,
}

# Prefixes of all currently supported devices
DEVICE_NAME_RE = re.compile(
    r"^(AC2A|AC60|AC60P|AC70|AC70P|AC180|AC180P|AC200L|AC200M|AC200PL|AC300|AC500|EB3A|EP500|EP500P|EP600|EP760|EP800|Handsfree\ 1)(\d+)$"
)
