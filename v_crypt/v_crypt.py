"""
    Encrypt/Decrypt functions using Fernet.

    You can encrypt a string with:
        encryption.encrypt("secret", key)

    And then you can decrypt it with:
        value = encryption.decrypt(crypted_string, key)

    In order to do that you'll need an environ var or a txt with the secret.
    
    To create a master password:
        encryption.create_password()
"""

import utils as u

from defaults import FILE_MASTER_DEFAULT, FILE_SECRETS_DEFAULT_JSON, STORE_SECRET


class Cipher:
    """docstring for ClassName"""

    def __init__(self, **kwa):
        """
            Create a cipher instance

            Args:
                filename_master_password:   filename of the master password
                secrets_file:               filename of the dictionary with secrets
                environ_var_name:           name of the environ variable
        """

        # Save secrets filename
        self.secrets_file = kwa.get("secrets_file", FILE_SECRETS_DEFAULT_JSON)

        self.filename_master_password = kwa.get("filename_master_password", FILE_MASTER_DEFAULT)
        self.environ_var_name = kwa.get("environ_var_name", None)

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

    def get_secret(self, key):
        """
            Read one secret from the dict of secrets.

            Args:
                key:    id of the secret

            Returns:
                the secret as a string
        """

        return u.get_secret(
            key,
            password=u.get_password(self.filename_master_password, self.environ_var_name),
            secrets_file=self.secrets_file,
        )

    def create_password(self, store_secret):
        """
            Creates a new master password.

            Args:
                store_secret:   boolean to decide if master password should be stored in a file
        """

        u.create_password(self.filename_master_password, store_secret)
