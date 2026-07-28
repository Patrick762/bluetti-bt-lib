import unittest

from bluetti_bt_lib.bluetooth.encryption import BluettiEncryption, Message


class TestV1(unittest.TestCase):
    def setUp(self):
        self.enc = BluettiEncryption()
        self.challenge = Message(bytearray([0x2a, 0x2a, 0x00, 0x00, 66, 73, 84, 69, 0x00, 0x00]))

    def test_msg_challenge(self):
        result = self.enc.msg_challenge(self.challenge)

        self.assertEqual(self.enc.unsecure_aes_iv.hex(), "387baabfdda065260b8bcd59a9b0f9c8")
        self.assertEqual(self.enc.unsecure_aes_key.hex(), "7de46f8a5d2924d77b1a2dc0975310f5")
        self.assertEqual(result.hex(), "2a2a02040b8bcd5901c2")
