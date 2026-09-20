import requests
from os.path import join

url = "https://patrick762.github.io/bluetti-registers/devices.json"

output = "bluetti_bt_lib/devices/"
output_base = "bluetti_bt_lib/base_devices/"
output_fields = "bluetti_bt_lib/fields/"

print("Loading devices list")

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
field_names_list: list[str] = []

for d in devices_json:
    if d["comm_type"] != "bt":
        continue

    name = d["name"]

    if name == "BT1":
        name = "BaseDeviceV1"
    elif name == "BT2":
        name = "BaseDeviceV2"

    file_name = str(name).lower().replace(" ", "") + ".py"
    fields = ""

    if str(name).startswith("Handsfree"):
        device_names.append(str(name).replace(" ", "\\s"))
    else:
        device_names.append(str(name).replace(" ", ""))

    for f in d["fields"]:
        fields += f'\n\t\t\t\t{get_type(str(f["datatype"]))}(FieldName.{str(f["name"]).upper()}, {f["start"]}{get_params(f)}),'

        if f["name"] not in field_names_list:
            field_names_list.append(f["name"])

    content = f"""from ..base_devices import BluettiDevice
from ..fields import *

# GENERATED FILE! ONLY EDIT FOR TESTING!


class {str(name).replace(" ", "")}(BluettiDevice):
    def __init__(self):
        super().__init__(
            [{fields}
            ]
        )
""".replace(
        "\t", "    "
    )

    if name in ["BaseDeviceV1", "BaseDeviceV2"]:
        output_dir = output_base
    else:
        output_dir = output

    with open(join(output_dir, file_name), "w") as f:
        f.write(content)

init_py = f"""# GENERATED FILE! ONLY EDIT FOR TESTING!

{"\n".join([f"from .{d.lower().replace("\\s", "")} import *" if d not in ["BaseDeviceV1", "BaseDeviceV2"] else f"# Ignored {d}" for d in device_names])}

DEVICES = {{
\t{"\n\t".join([f"\"{d.replace("\\s", " ")}\": {d.replace("\\s", "")}," if d not in ["BaseDeviceV1", "BaseDeviceV2"] else f"# Ignored {d}" for d in device_names])}
}}
""".replace(
    "\t", "    "
)

with open(join(output, "__init__.py"), "w") as f:
    f.write(init_py)

field_names = [f'{fn.upper()} = "{fn}"' for fn in field_names_list]

field_name_py = f"""# GENERATED FILE! ONLY EDIT FOR TESTING!

from enum import Enum, unique


@unique
class FieldName(Enum):
    {"\n\t".join(field_names)}
""".replace(
    "\t", "    "
)

with open(join(output_fields, "field_name.py"), "w") as f:
    f.write(field_name_py)
