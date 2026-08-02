import unittest

from bluetti_bt_lib.bluetooth.encryption import BluettiEncryption, Message


class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.enc = BluettiEncryption()
        self.challenge = Message(bytes.fromhex("2a2a01042d61a7cf0209"))
        self.data_pre = Message(bytes.fromhex("0086ee8d0951524cef340de225cf73fc3c7f7f2c0ae6dd4fb9a53c8e1216216898aa8f38053227594babe787c0c4f644bad5c8d6359ea8021dcd147d29edbfe60e22acb28839204a3db511581e306f65bed5bc977ea8230e42587d1c52db4e645ec23e913f094a80a4c87bced44d37b1da70b893a4f2e67c398edfc36dc411ec354856d43f4849211875b29d711811afdf75"))

    def test_msg_challenge(self):
        result = self.enc.msg_challenge(self.challenge)

        self.assertEqual(self.enc.unsecure_aes_iv.hex(), "896ae63a17142513e81b95f4e9d2f194")
        self.assertEqual(self.enc.unsecure_aes_key.hex(), "ccf5230f979d64e2988a756dd73118a9")
        self.assertEqual(result.hex(), "2a2a0204e81b95f40292")

    def test_decrypt_pre_key_exchange(self):
        # Init IV and key
        self.enc.msg_challenge(self.challenge)

        key, iv = self.enc.getKeyIv()

        decrypted = self.enc.aes_decrypt(self.data_pre.buffer, key, iv)

        self.assertEqual(decrypted.hex(), "2a2a04803dfa514fd94519d9aea481b8c617850e8f6da8d75ac01d08bcefb9ab0cd911dadbe89fe698ba331bb7ee51e42888bc043a601969958646e3a8f4851e3170ff4ccf157f4365444bb58830957e52cc671e160ad13ef8ae33558e927347cbba35f9fcd148fa6f6f83aa2baf126cbefae6bde4ab75259bace02b9fbdc3274aa09e1d4296")

