import json
import os
from pathlib import Path

import yaml
from loguru import logger

from vcrypto.encryption import decrypt
from vcrypto.encryption import encrypt

# Default file names
FILE_MASTER_DEFAULT = "master.password"
FILE_SECRETS_DEFAULT = "secrets.yaml"


def get_password(filename=FILE_MASTER_DEFAULT, environ_var_name=None):
    """
    Retrieves the master password. By default, it reads from a file.
    It can also be retrieved from an environment variable.

    Args:
        filename (str): Name of the file containing the master password.
        environ_var_name (str): Environment variable name storing the password.

    Returns:
        bytes: The password, or None if not found.
    """
    if environ_var_name:
        password = os.getenv(environ_var_name)
        if password:
            return password.encode()
        logger.error(f"Environment variable {environ_var_name} not found")
        return None

    path = Path(filename)
    if path.exists():
        return path.read_text().strip().encode()

    logger.error(f"{filename=} not found")
    return None


def _is_json(path):
    valid_extensions = {"json", "yaml", "yml"}
    extension = path.suffix.lstrip(".")

    assert extension in valid_extensions, f"{extension=} must be in {valid_extensions=}"

    return extension == "json"


def store_dictionary(data, filename):
    """
    Stores a dictionary in a JSON or YAML file.

    Args:
        data (dict): Dictionary to store.
        filename (str): Destination file.
    """

    path = Path(filename)

    if _is_json(path):
        text = json.dumps(data, indent=2)

    else:
        text = yaml.dump(data)

    path.write_text(text, encoding="utf-8")


def read_dictionary(filename):
    """
    Reads a dictionary from a JSON or YAML file.

    Args:
        filename (str): File to read.

    Returns:
        dict: Parsed dictionary.
    """
    path = Path(filename)

    if not path.exists():
        raise ValueError(f"{filename=} does not exist")

    content = path.read_text(encoding="utf-8")

    if _is_json(path):
        return json.loads(content)
    else:
        return yaml.safe_load(content)


def save_secret(key, value, password=None, secrets_file=FILE_SECRETS_DEFAULT):
    """
    Adds a secret to the encrypted secrets file.

    Args:
        key (str): Identifier for the secret.
        value (str): Value to store.
        password (bytes, optional): Encryption password. Defaults to master password.
        secrets_file (str): Path to the secrets file.
    """
    logger.debug(f"Storing secret {key=}")

    password = password or get_password()
    if password is None:
        raise ValueError("No password found. Cannot save secret")

    data = read_dictionary(secrets_file)
    data[key] = encrypt(value, password)

    store_dictionary(data, secrets_file)
    logger.debug(f"Secret {key=} saved")


def get_secret(key, password=None, encoding="utf-8", secrets_file=FILE_SECRETS_DEFAULT):
    """
    Retrieves a secret from the encrypted secrets file.

    Args:
        key (str): Identifier of the secret.
        password (bytes, optional): Decryption password. Defaults to master password.
        encoding (str, optional): Encoding for the decrypted value. Defaults to "utf-8".
        secrets_file (str): Path to the secrets file.

    Returns:
        str | bytes | None: The decrypted value, or None if not found.
    """
    logger.debug(f"Reading secret {key=}")

    password = password or get_password()
    if password is None:
        raise ValueError("No password found. Cannot save secret")

    data = read_dictionary(secrets_file)
    if key not in data:
        raise ValueError(f"Secret '{key}' not found in {secrets_file}")

    out = decrypt(data[key], password, encoding)
    logger.debug(f"Secret {key=} read")
    return out
