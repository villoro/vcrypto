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


if __name__ == "__main__":
    unittest.main()
