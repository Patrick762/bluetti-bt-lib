from enum import Enum
import unittest
from bluetti_bt_lib.base_devices import BluettiDevice
from bluetti_bt_lib.fields import (
    BoolField,
    EnumField,
    SelectField,
    StringField,
    SerialNumberField,
    FieldName,
    SwitchField,
)
from bluetti_bt_lib.registers import ReadableRegisters


class Dummy(Enum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2


class TestBluettiDevice(unittest.TestCase):
    def test_get_registers_empty(self):
        device = BluettiDevice(fields=[], pack_fields=[], max_packs=0)

        registers = device.get_polling_registers()
        self.assertEqual(registers, [])

        pack_registers = device.get_pack_polling_registers()
        self.assertEqual(pack_registers, [])

    def test_get_empty_fields(self):
        device = BluettiDevice(fields=[], pack_fields=[], max_packs=0)

        self.assertEqual(device.get_bool_fields(), [])
        self.assertEqual(device.get_switch_fields(), [])
        self.assertEqual(device.get_select_fields(), [])
        self.assertEqual(device.get_sensor_fields(), [])

    def test_not_implemented_methods(self):
        device = BluettiDevice(fields=[], pack_fields=[], max_packs=0)

        with self.assertRaises(NotImplementedError):
            device.get_full_registers_range()

        with self.assertRaises(NotImplementedError):
            device.get_device_type_registers()

        with self.assertRaises(NotImplementedError):
            device.get_device_sn_registers()

        with self.assertRaises(NotImplementedError):
            device.get_iot_version()

        with self.assertRaises(NotImplementedError):
            device.get_pack_selector(1)

    def test_parse(self):
        # TODO: Implement test for parse method
        pass

    def test_build_write_command(self):
        # TODO: Implement test for build_write_command method
        pass

    def test_initialization_with_fields(self):
        fields = [
            StringField(FieldName.DEVICE_TYPE, 200, 6),
            SerialNumberField(FieldName.DEVICE_SN, 100),
            BoolField(FieldName.CTRL_AC, 150),
        ]
        pack_fields = [
            StringField(FieldName.PACK_TYPE, 300, 6),
        ]

        device = BluettiDevice(fields=fields, pack_fields=pack_fields, max_packs=2)

        polling_registers = device.get_polling_registers()
        self.assertEqual(len(polling_registers), 3)
        self.assertIsInstance(polling_registers[0], ReadableRegisters)
        self.assertIsInstance(polling_registers[1], ReadableRegisters)
        self.assertIsInstance(polling_registers[2], ReadableRegisters)

        # Check if sorted correctly by address
        self.assertEqual(polling_registers[0].starting_address, 100)
        self.assertEqual(polling_registers[1].starting_address, 150)
        self.assertEqual(polling_registers[2].starting_address, 200)

        pack_polling_registers = device.get_pack_polling_registers()
        self.assertEqual(len(pack_polling_registers), 1)
        self.assertIsInstance(pack_polling_registers[0], ReadableRegisters)
        self.assertEqual(pack_polling_registers[0].starting_address, 300)

        sensor_fields = device.get_sensor_fields()
        self.assertEqual(len(sensor_fields), 2)

        bool_fields = device.get_bool_fields()
        self.assertEqual(len(bool_fields), 1)

    def test_switch_fields(self):
        fields = [
            SwitchField(FieldName.CTRL_AC, 150),
            BoolField(FieldName.CTRL_DC, 160),
        ]

        device = BluettiDevice(fields=fields, pack_fields=[], max_packs=0)

        self.assertEqual(len(device.get_switch_fields()), 1)
        self.assertEqual(len(device.get_bool_fields()), 1)

    def test_select_fields(self):
        fields = [
            SelectField(FieldName.CTRL_CHARGING_MODE, 180, Dummy),
            EnumField(FieldName.AC_OUTPUT_MODE, 70, Dummy),
        ]

        device = BluettiDevice(fields=fields, pack_fields=[], max_packs=0)

        self.assertEqual(len(device.get_select_fields()), 1)
        self.assertEqual(len(device.get_sensor_fields()), 1)
