from loguru import logger

from vcrypto import encryption
from vcrypto import secrets_manager as sm

# Global instance for Singleton
_VCRYPTO = None


class Vcrypto:
    """Singleton class to manage encryption and secrets storage."""

    def __init__(self, secrets_file, filename_master_password, environ_var_name=None):
        """
        Initialize the Vcrypto instance.

        Args:
            secrets_file (str): Path to the secrets storage file.
            filename_master_password (str): Path to the master password file.
            environ_var_name (str, optional): Name of the environment variable for the master password.
        """
        self.secrets_file = secrets_file
        self.filename_master_password = filename_master_password
        self.environ_var_name = environ_var_name

    def _get_password(self):
        """Retrieve the master password (from file or environment variable)."""
        return sm.get_password(self.filename_master_password, self.environ_var_name)

    def save_secret(self, key, value):
        """Encrypt and store a secret."""
        password = self._get_password()
        sm.save_secret(key, value, password, secrets_file=self.secrets_file)

    def get_secret(self, key, encoding="utf8"):
        """Retrieve a decrypted secret."""
        password = self._get_password()
        return sm.get_secret(key, password, self.secrets_file, encoding=encoding)

    def create_password(self, store_secret=True):
        """Create and store a master password."""
        return encryption.create_password(self.filename_master_password, store_secret)

    @staticmethod
    def _check_vcrypto():
        """Ensure Vcrypto is initialized before calling any function."""
        if _VCRYPTO is None:
            raise RuntimeError("Vcrypto is not initialized. Call init_vcrypto() first.")


def init_vcrypto(
    secrets_file="secrets.json",
    filename_master_password="master.password",
    environ_var_name=None,
):
    """Initialize the Vcrypto singleton globally."""
    global _VCRYPTO

    if _VCRYPTO is None:
        logger.debug("Initialzying vcrypto")
        _VCRYPTO = Vcrypto(secrets_file, filename_master_password, environ_var_name)
    else:
        logger.warning("Vcrypto has already been initialized!")


def get_secret(key, encoding="utf8"):
    """Global function to retrieve a secret."""
    Vcrypto._check_vcrypto()
    return _VCRYPTO.get_secret(key, encoding)


def save_secret(key, value):
    """Global function to store a secret."""
    Vcrypto._check_vcrypto()
    _VCRYPTO.save_secret(key, value)


def create_password(store_secret=True):
    """Global function to create a master password."""
    Vcrypto._check_vcrypto()
    return _VCRYPTO.create_password(store_secret)
