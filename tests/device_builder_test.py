import unittest

from bluetti_bt_lib.utils.device_builder import build_device
from bluetti_bt_lib.devices import DEVICES


class TestDeviceBuilder(unittest.TestCase):
    def test_build(self):
        for name, cls in DEVICES.items():
            built = build_device(name + "12345678")
            self.assertIsInstance(built, cls)
