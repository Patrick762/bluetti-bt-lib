from enum import Enum, unique


@unique
class FieldName(Enum):
    AC_INPUT_POWER = "ac_input_power"
    AC_INPUT_VOLTAGE = "ac_input_voltage"
    AC_OUTPUT_ON = "ac_output_on"
    AC_OUTPUT_POWER = "ac_output_power"
    BATTERY_SOC = "total_battery_percent"
    DC_INPUT_POWER = "dc_input_power"
    DC_OUTPUT_ON = "dc_output_on"
    DC_OUTPUT_POWER = "dc_output_power"
    DEVICE_TYPE = "device_type"
    POWER_GENERATION = "power_generation"
    POWER_LIFTING_ON = "power_lifting_on"
