# GENERATED FILE! ONLY EDIT FOR TESTING!

import re

from .ap300 import *
from .pr30v2 import *
from .ep600 import *
from .ac60 import *
from .ac70 import *
from .ac70p import *
from .ac200m import *
from .ac50b import *
from .ep800 import *
from .ac2a import *
from .el100v2 import *
from .ep500 import *
from .handsfree1 import *
from .ac200pl import *
from .ep760 import *
from .el10 import *
from .ac300 import *
from .ac200l import *
from .ac180t import *
from .ep2000 import *
from .ac500 import *
from .el30v2 import *
from .ep500p import *
from .eb3a import *
from .ac60p import *
from .ac180 import *
from .ac2p import *
from .ac180p import *

DEVICES = {
	"AP300": AP300,
	"PR30V2": PR30V2,
	"EP600": EP600,
	"AC60": AC60,
	"AC70": AC70,
	"AC70P": AC70P,
	"AC200M": AC200M,
	"AC50B": AC50B,
	"EP800": EP800,
	"AC2A": AC2A,
	"EL100V2": EL100V2,
	"EP500": EP500,
	"Handsfree 1": Handsfree1,
	"AC200PL": AC200PL,
	"EP760": EP760,
	"EL10": EL10,
	"AC300": AC300,
	"AC200L": AC200L,
	"AC180T": AC180T,
	"EP2000": EP2000,
	"AC500": AC500,
	"EL30V2": EL30V2,
	"EP500P": EP500P,
	"EB3A": EB3A,
	"AC60P": AC60P,
	"AC180": AC180,
	"AC2P": AC2P,
	"AC180P": AC180P,
}

DEVICE_NAME_RE = re.compile(
    r"^(AP300|PR30V2|EP600|AC60|AC70|AC70P|AC200M|AC50B|EP800|AC2A|EL100V2|EP500|Handsfree\s1|AC200PL|EP760|EL10|AC300|AC200L|AC180T|EP2000|AC500|EL30V2|EP500P|EB3A|AC60P|AC180|AC2P|AC180P)(\d+)$"
)
