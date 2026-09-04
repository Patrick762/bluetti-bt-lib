import requests

tag = "0.0.22"
url = f"https://github.com/Patrick762/bluetti-registers/releases/download/{tag}/bluetooth.json"

output = "bluetti_bt_lib/devices/"

print("Loading devices list schema")

schema = requests.get(url).json()


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def get_type(t: str):
    match(t):
        case "bool":
            return "BoolField"
        case "enum":
            return "EnumField"
        case "serial":
            return "SerialNumberField"
        case "string":
            return "StringField"
        case "swstring":
            return "SwapStringField"
        case "uint":
            return "UIntField"
        case "uint16":
            return "UIntField"
        case "uint32":
            return "UIntField"
        case "version":
            return "VersionField"

    return "UINT16"

def get_params(f):
    # TODO
    return ""

device_names: list[str] = []

for d in schema:
    name = d["name"]
    file_name = str(name).lower().replace(" ", "") + ".py"
    fields = ""

    if str(name).startswith("Hands"):
        device_names.append(str(name).replace(" ", "\\s"))
    else:
        device_names.append(str(name).replace(" ", ""))

    for f in d["fields"]:
        fields += f'\n\t\t\t{get_type(str(f["content"]))}("{f["name"]}", {f["address"]}{get_params(f)}),'

    content = f"""from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!

class {str(name).replace(" ", "")}(BluettiDevice):
    def __init__(self):
        super().__init__([{fields}
        ])
"""

    with open(output + file_name, "w") as f:
        f.write(content)

init_py = f"""# GENERATED FILE! ONLY EDIT FOR TESTING!

import re

{"\n".join([f"from .{d.lower().replace("\\s", "")} import *" for d in device_names])}

DEVICES = {{
\t{"\n\t".join([f"\"{d.replace("\\s", " ")}\": {d.replace("\\s", "")}," for d in device_names])}
}}

DEVICE_NAME_RE = re.compile(
    r"^({"|".join([(n.upper() if "\\s" not in n else n) for n in device_names])})(\\d+)$"
)
"""

with open(output + "__init__.py", "w") as f:
    f.write(init_py)
