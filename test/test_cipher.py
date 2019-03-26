"""
    Tests for v_crypt.py
"""

import os
import unittest

from v_crypt.v_crypt import Cipher


class TestCipher(unittest.TestCase):
    """Test v_crypt Cipher"""

    key = "secret"
    secret = "hello"

    secrets_file = "temp_secrets.json"
    master_password = "temp.password"

    cipher = Cipher(secrets_file=secrets_file, filename_master_password=master_password)

    def test_save_secret(self):
        """ Test that is able to store a secret """

        self.cipher.create_password(store_secret=True)
        self.cipher.save_secret(self.key, self.secret)

    def test_read_secret(self):
        """ Test read/write of dictionaries """

        self.cipher.create_password(store_secret=True)
        self.cipher.save_secret(self.key, self.secret)

        self.assertEqual(self.secret, self.cipher.get_secret(self.key))


if __name__ == "__main__":
    unittest.main()
