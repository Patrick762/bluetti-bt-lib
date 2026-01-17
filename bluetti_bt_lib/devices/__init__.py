import re

from .ac2a import AC2A
from .ac50b import AC50B
from .ac60 import AC60
from .ac60p import AC60P
from .ac70 import AC70
from .ac70p import AC70P
from .ac180 import AC180
from .ac180p import AC180P
from .ac180t import AC180T
from .ac200l import AC200L
from .ac200m import AC200M
from .ac200pl import AC200PL
from .ac300 import AC300
from .ac500 import AC500
from .ap300 import AP300
from .eb3a import EB3A
from .el100v2 import EL100V2
from .el30v2 import EL30V2
from .ep500 import EP500
from .ep500p import EP500P
from .ep600 import EP600
from .ep800 import EP800
from .ep2000 import EP2000
from .handsfree1 import Handsfree1

# Add new device classes here
DEVICES = {
    "AC2A": AC2A,
    "AC50B": AC50B,
    "AC60": AC60,
    "AC60P": AC60P,
    "AC70": AC70,
    "AC70P": AC70P,
    "AC180": AC180,
    "AC180T": AC180T,
    "AC180P": AC180P,
    "AC200L": AC200L,
    "AC200M": AC200M,
    "AC200PL": AC200PL,
    "AC300": AC300,
    "AC500": AC500,
    "AP300": AP300,
    "EB3A": EB3A,
    "EL100V2": EL100V2,
    "EL30V2": EL30V2,
    "EP500": EP500,
    "EP500P": EP500P,
    "EP600": EP600,
    "EP800": EP800,
    "EP2000": EP2000,
    "Handsfree 1": Handsfree1,
}

# Prefixes of all currently supported devices
DEVICE_NAME_RE = re.compile(
    r"^(AC2A|AC50B|AC60|AC60P|AC70|AC70P|AC180|AC180T|AC180P|AC200L|AC200M|AC200PL|AC300|AC500|AP300|EB3A|EL100V2|EL30V2|EP500|EP500P|EP600|EP760|EP800|EP2000|Handsfree\s1)(\d+)$"
)
