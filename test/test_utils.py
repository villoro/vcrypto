"""
    Tests for utilities.py
"""

import unittest

from v_crypt import utilities as u


class TestUtilities(unittest.TestCase):
    """Test utilities"""

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


if __name__ == "__main__":
    unittest.main()
