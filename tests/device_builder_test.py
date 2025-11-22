import unittest

from src.utils.device_builder import build_device
from src.devices import DEVICES


class TestDeviceBuilder(unittest.TestCase):
    def test_build(self):
        for name, cls in DEVICES.items():
            built = build_device(name + "12345678")
            self.assertIsInstance(built, cls)
