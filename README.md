# bluetti-bt-lib
Inofficial Library for basic communication to bluetti powerstations.
Core functions based on https://github.com/warhammerkid/bluetti_mqtt

The current [Roadmap for this project and repositories using this library can be found here](https://github.com/users/Patrick762/projects/4)

## Disclaimer
This library is provided without any warranty or support by Bluetti. I do not take responsibility for any problems it may cause in all cases. Use it at your own risk.

## Projects using this library

- [Home Assistant Integration](https://github.com/Patrick762/hassio-bluetti-bt)
- MQTT Server (planned)
- [UPS Server (NUT compatible)](https://github.com/Patrick762/nut-server-bluetti)

## Supported Powerstations and data

Validated

|Device Name|total_battery_percent|dc_input_power|ac_input_power|dc_output_power|ac_output_power|
|-----------|---------------------|--------------|--------------|---------------|---------------|
|AC70       |✅                   |✅            |✅            |✅             |✅             |
|AC180      |✅                   |✅            |✅            |✅             |✅             |
|EB3A       |✅                   |✅            |✅            |✅             |✅             |
|EP600      |✅                   |PV            |Grid          |❌             |AC Phases      |
|Handsfree 1|✅                   |✅            |✅            |✅             |✅             |

Added and mostly validated by contributors (some are moved here from the HA Integration https://github.com/Patrick762/hassio-bluetti-bt):

|Device Name|Contributor     |total_battery_percent|dc_input_power|ac_input_power|dc_output_power|ac_output_power|
|-----------|----------------|---------------------|--------------|--------------|---------------|---------------|
|AC2A       |@ruanmed        |✅                   |✅            |✅            |✅             |✅             |
|AC50B      |@goetzc         |✅                   |❌            |✅            |✅             |✅             |
|AC60       |@mzpwr          |✅                   |✅            |✅            |✅             |✅             |
|AC60P      |@mzpwr          |✅                   |✅            |✅            |✅             |✅             |
|AC70P      |@matthewpucc    |✅                   |✅            |✅            |✅             |✅             |
|AC180P     |@Patrick762     |✅                   |✅            |✅            |✅             |✅             |
|AC200L     |bluetti-mqtt    |✅                   |✅            |✅            |✅             |✅             |
|AC200M     |bluetti-mqtt    |✅                   |✅            |✅            |✅             |✅             |
|AC200PL    |@0x4E4448       |✅                   |✅            |✅            |✅             |✅             |
|AC300      |bluetti-mqtt    |✅                   |✅            |✅            |✅             |✅             |
|AC500      |bluetti-mqtt    |✅                   |✅            |✅            |✅             |✅             |
|AP300      |@seaburger      |✅                   |✅            |✅            |❌             |✅             |
|EL30V2     |@dgudim         |✅                   |✅            |✅            |✅             |✅             |
|EL100V2    |@seaburger      |✅                   |✅            |✅            |✅             |✅             |
|EP500      |bluetti-mqtt    |✅                   |✅            |✅            |✅             |✅             |
|EP500P     |bluetti-mqtt    |✅                   |✅            |✅            |✅             |✅             |
|EP760      |@Apfuntimes     |✅                   |PV            |Grid          |❌             |AC Phases      |
|EP800      |@jhagenk        |✅                   |❌            |❌            |❌             |❌             |

## Controls

Currently only "switches" are supported

Validated

|Device Name|ctrl_ac|ctrl_dc|
|-----------|-------|-------|
|EB3A       |✅     |✅     |

## Battery pack data

Data for battery packs will no longer be available in this library

## Installation

```bash
pip install bluetti-bt-lib
```

## Commands for testing

Commands included in this library should only be used for testing.

### Scan for supported devices

```bash
usage: bluetti-scan [-h]

Detect bluetti devices by bluetooth name

options:
  -h, --help  show this help message and exit
```

Example output: `['EB3A', '00:00:00:00:00:00']`

### Detect device type by mac address

```bash
usage: bluetti-detect [-h] mac

Detect bluetti devices

positional arguments:
  mac         Mac-address of the powerstation

options:
  -h, --help  show this help message and exit
```

Example:

```bash
bluetti-detect 00:00:00:00:00:00
```

Example output: `Device type is 'EB3A' with iot version 1 and serial 0000000000000. Full name: EB3A0000000000000`

### Read device data for supported devices

```bash
usage: bluetti-read [-h] [-m MAC] [-t TYPE] [-e ENCRYPTION]

Detect bluetti devices

options:
  -h, --help            show this help message and exit
  -m MAC, --mac MAC     Mac-address of the powerstation
  -t TYPE, --type TYPE  Type of the powerstation (AC70 f.ex.)
  -e ENCRYPTION, --encryption ENCRYPTION
                        Add this if encryption is needed
```

Example:

```bash
bluetti-read -m 00:00:00:00:00:00 -t EB3A
```

Example output:
```bash
FieldName.DEVICE_TYPE: EB3A
FieldName.DEVICE_SN: 0000000000000
FieldName.BATTERY_SOC: 92%
FieldName.DC_INPUT_POWER: 0W
FieldName.AC_INPUT_POWER: 0W
FieldName.AC_OUTPUT_POWER: 0W
FieldName.DC_OUTPUT_POWER: 0W
FieldName.CTRL_AC: False
FieldName.CTRL_DC: True
FieldName.CTRL_LED_MODE: LedMode.OFF
FieldName.CTRL_POWER_OFF: False
FieldName.CTRL_ECO: False
FieldName.CTRL_ECO_TIME_MODE: EcoMode.HOURS1
FieldName.CTRL_CHARGING_MODE: ChargingMode.STANDARD
FieldName.CTRL_POWER_LIFTING: False
```

### Write to supported device

INFO: Devices with encryption are currently not supported!

```bash
usage: bluetti-write [-h] [-m MAC] [-t TYPE] [--on ON] [--off OFF] [-v VALUE] [-e ENCRYPTION] field

Write to bluetti device

positional arguments:
  field                 Field name (ctrl_dc f.ex.)

options:
  -h, --help            show this help message and exit
  -m MAC, --mac MAC     Mac-address of the powerstation
  -t TYPE, --type TYPE  Type of the powerstation (AC70 f.ex.)
  --on ON               Value to write
  --off OFF             Value to write
  -v VALUE, --value VALUE
                        Value to write (integer, see enum for value)
  -e ENCRYPTION, --encryption ENCRYPTION
                        Add this if encryption is needed
```

Example:

```bash
bluetti-write -m 00:00:00:00:00:00 -t EB3A --on on ctrl_ac
```

## Adding fields

To add new fields, you can use the `bluetti-detect` command to first find out which version of iot protocol is used and if it uses encryption.

After you got this information, you can use the `bluetti-readall` command to read every registry and save the data to a json file. You should also note all values you see in the app to later compare the data.

Here's how to use the `bluetti-readall` command:

```bash
usage: bluetti-readall [-h] [-m MAC] [-v VERSION] [-e ENCRYPTION]

Detect bluetti devices

options:
  -h, --help            show this help message and exit
  -m MAC, --mac MAC     Mac-address of the powerstation
  -v VERSION, --version VERSION
                        IoT protocol version
  -e ENCRYPTION, --encryption ENCRYPTION
                        Add this if encryption is needed
```

With the separate tool at [bluetti-bt-raw-reader](https://github.com/Patrick762/bluetti-bt-raw-reader) you can view those values in a more understandable way.

You can also share the output with me using [this form](https://forms.gle/ewp7DYigtaN3ZLc68)


To test added fields with the created json file, use `bluetti-parse`:

```bash
usage: bluetti-parse [-h] file

Parse readall output files

positional arguments:
  file        JSON file of the powerstation readall output

options:
  -h, --help  show this help message and exit
```
