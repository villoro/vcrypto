"""
    Encrypt/Decrypt functions using Fernet.

    Initialize:
        cipher = Cipher()

    You can encrypt a string with:
        cipher.encrypt("secret", key)

    And then you can decrypt it with:
        value = cipher.decrypt(crypted_string, key)

    In order to do that you'll need an environ var or a txt with the secret.

    To create a master password:
        cipher.create_password()
"""

from . import utilities as u

from .defaults import FILE_MASTER_DEFAULT
from .defaults import FILE_SECRETS_DEFAULT_JSON
from .defaults import STORE_SECRET


class Cipher:
    """docstring for ClassName"""

    def __init__(
        self,
        secrets_file=FILE_SECRETS_DEFAULT_JSON,
        filename_master_password=FILE_MASTER_DEFAULT,
        environ_var_name=None,
    ):
        """
            Create a cipher instance

            Args:
                filename_master_password:   filename of the master password
                secrets_file:               filename of the dictionary with secrets
                environ_var_name:           name of the environ variable
        """

        # Save secrets filename
        self.secrets_file = secrets_file
        self.filename_master_password = filename_master_password
        self.environ_var_name = environ_var_name

    def save_secret(self, key, value):
        """
            Add one secret in the dict of secrets. It will create the dict if needed

            Args:
                key:    id of the secret
                value:  what to store
        """

        u.save_secret(
            key,
            value,
            password=u.get_password(self.filename_master_password, self.environ_var_name),
            secrets_file=self.secrets_file,
        )

    def get_secret(self, key, encoding="utf8"):
        """
            Read one secret from the dict of secrets.

            Args:
                key:        id of the secret
                encoding:   encoding to use for decoding bytes [if None returns bytes]

            Returns:
                the secret as a string
        """

        return u.get_secret(
            key,
            password=u.get_password(self.filename_master_password, self.environ_var_name),
            secrets_file=self.secrets_file,
            encoding=encoding,
        )

    def create_password(self, store_secret=STORE_SECRET):
        """
            Creates a new master password.

            Args:
                store_secret:   boolean to decide if master password should be stored in a file
        """

        return u.create_password(self.filename_master_password, store_secret)
