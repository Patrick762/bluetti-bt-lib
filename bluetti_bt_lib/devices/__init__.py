# GENERATED FILE! ONLY EDIT FOR TESTING!

import re

from .ac2p import *
from .eb3a import *
from .ac2a import *
from .ap300 import *
from .ac180t import *
from .el30v2 import *
from .el10 import *
from .ac70p import *
from .pr30v2 import *
from .ac500 import *
from .ep760 import *
from .el100v2 import *
from .ep500p import *
from .ep500 import *
from .ac180 import *
from .ac200l import *
from .ac300 import *
from .ep600 import *
from .ac200pl import *
from .handsfree2 import *
from .ac70 import *
from .ac60 import *
from .ep2000 import *
from .handsfree1 import *
from .ac60p import *
from .ac180p import *
from .pr100v2 import *
from .ac200m import *
from .ep800 import *
from .ac50b import *

DEVICES = {
    "AC2P": AC2P,
    "EB3A": EB3A,
    "AC2A": AC2A,
    "AP300": AP300,
    "AC180T": AC180T,
    "EL30V2": EL30V2,
    "EL10": EL10,
    "AC70P": AC70P,
    "PR30V2": PR30V2,
    "AC500": AC500,
    "EP760": EP760,
    "EL100V2": EL100V2,
    "EP500P": EP500P,
    "EP500": EP500,
    "AC180": AC180,
    "AC200L": AC200L,
    "AC300": AC300,
    "EP600": EP600,
    "AC200PL": AC200PL,
    "Handsfree 2": Handsfree2,
    "AC70": AC70,
    "AC60": AC60,
    "EP2000": EP2000,
    "Handsfree 1": Handsfree1,
    "AC60P": AC60P,
    "AC180P": AC180P,
    "PR100V2": PR100V2,
    "AC200M": AC200M,
    "EP800": EP800,
    "AC50B": AC50B,
}

DEVICE_NAME_RE = re.compile(
    r"^(AC2P|EB3A|AC2A|AP300|AC180T|EL30V2|EL10|AC70P|PR30V2|AC500|EP760|EL100V2|EP500P|EP500|AC180|AC200L|AC300|EP600|AC200PL|Handsfree\s2|AC70|AC60|EP2000|Handsfree\s1|AC60P|AC180P|PR100V2|AC200M|EP800|AC50B)(\d+)$"
)
