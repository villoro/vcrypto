"""
    Tests for encryption.py
"""

import unittest

from v_crypt import encryption as enc


class TestEncryption(unittest.TestCase):
    """Test encryption"""

    def test_store_secret(self):
        """ Test password creation with storing """

        self.assertIsNotNone(enc.create_password(filename="temp.password"))

    def test_encrypt(self):
        """ Test that is able to encrypt a secret """

        password = enc.create_password(store_secret=False)
        enc.encrypt("my_secret", password)

    def test_decrypt(self):
        """ Test that by encrypting and decrypting the string is not modified """

        password = enc.create_password(store_secret=False)
        secret = enc.encrypt("my_secret", password)

        self.assertEqual(enc.decrypt(secret, password), "my_secret")


if __name__ == "__main__":
    unittest.main()
