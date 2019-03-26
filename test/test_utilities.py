"""
    Tests for utilities.py
"""

import os
import unittest

from v_crypt import utilities as u


class TestUtilities(unittest.TestCase):
    """Test utilities"""

    key = "secret"
    secret = "hello"

    mdict = {key: secret}

    file_secrets = "temp_secrets.json"

    def test_get_password(self):
        """ Test that is able to retrive a master password """

        # Test invalid environ var
        self.assertIsNone(u.get_password(environ_var_name="imaginary_env_var"))

        # Test invalid file
        self.assertIsNone(u.get_password(filename="imaginary_file.password"))

        # Retrive from file
        u.create_password(filename="test.password")
        self.assertEqual(type(u.get_password(filename="test.password")), bytes)

        # Retrive from env var
        self.assertEqual(type(u.get_password(environ_var_name="SECRET_TEST")), bytes)

    def test_dictionaries(self):
        """ Test read/write of dictionaries """

        # Test correct reading of json
        u.store_dictionary(self.mdict, self.file_secrets)
        u.read_dictionary(filename="temp.password")

        # Test correct reading of yaml
        u.store_dictionary(self.mdict, "temp_secrets.yaml")
        u.read_dictionary("temp_secrets.yaml")

    def test_read_write(self):
        """ Test that is possible to read and write secrets """

        password = u.create_password(store_secret=False)

        # Remove if file exists
        if os.path.isfile(self.file_secrets):
            os.remove(self.file_secrets)

        # Test it before and after file is created
        u.save_secret(self.key, self.secret, password=password, secrets_file=self.file_secrets)
        u.save_secret(self.key, self.secret, password=password, secrets_file=self.file_secrets)

        self.assertEqual(
            self.secret, u.get_secret(self.key, password=password, secrets_file=self.file_secrets)
        )

    def test_reading_errors(self):
        """ Test that it handles reading errors """

        password = u.create_password(store_secret=False)

        self.assertIsNone(u.get_secret(self.key, password, secrets_file="secrets_imaginary.json"))


if __name__ == "__main__":
    unittest.main()
