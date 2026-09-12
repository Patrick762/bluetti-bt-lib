import requests

url = "https://patrick762.github.io/bluetti-registers/devices.json"

output = "bluetti_bt_lib/devices/"

print("Loading devices list schema")

devices_json = requests.get(url).json()


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def get_type(t: str):
    match (t):
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
        case "version":
            return "VersionField"
        case "time":
            return "TimeField"

    return "#"


def get_params(f):
    # TODO
    return ""


device_names: list[str] = []

for d in devices_json:
    if d["comm_type"] != "bt":
        continue

    name = d["name"]
    file_name = str(name).lower().replace(" ", "") + ".py"
    fields = ""

    if str(name).startswith("Handsfree"):
        device_names.append(str(name).replace(" ", "\\s"))
    else:
        device_names.append(str(name).replace(" ", ""))

    for f in d["fields"]:
        fields += f'\n\t\t\t{get_type(str(f["datatype"]))}("{f["name"]}", {f["start"]}{get_params(f)}),'

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

{"\n".join([f"from .{d.lower().replace("\\s", "")} import *" for d in device_names])}

DEVICES = {{
\t{"\n\t".join([f"\"{d.replace("\\s", " ")}\": {d.replace("\\s", "")}," for d in device_names])}
}}
"""

with open(output + "__init__.py", "w") as f:
    f.write(init_py)
