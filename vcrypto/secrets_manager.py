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

# Supported extensions
VALID_EXTENSIONS = {"json", "yaml", "yml"}


def get_password(filename=FILE_MASTER_DEFAULT, environ_var_name=None):
    """
    Retrieves the master password from an environment variable or a file.

    Args:
        filename (str): Name of the file containing the master password.
        environ_var_name (str): Environment variable name storing the password.

    Returns:
        bytes: The password as bytes.

    Raises:
        ValueError: If no password is found.
    """
    if environ_var_name and (password := os.getenv(environ_var_name)):
        return password.encode()

    path = Path(filename)
    if path.exists():
        return path.read_text().strip().encode()

    raise ValueError(
        f"Password not found. Set {environ_var_name=} or create {filename=}"
    )


def _is_json(path: Path) -> bool:
    """
    Determines if a file has a JSON extension.

    Args:
        path (Path): File path.

    Returns:
        bool: True if the file is JSON, False if YAML.

    Raises:
        ValueError: If the file extension is invalid.
    """
    extension = path.suffix.lstrip(".")
    if extension not in VALID_EXTENSIONS:
        raise ValueError(f"Invalid {extension=}. Must be one of {VALID_EXTENSIONS=}")
    return extension == "json"


def store_dictionary(data: dict, filename: str):
    """
    Stores a dictionary in a JSON or YAML file.

    Args:
        data (dict): Dictionary to store.
        filename (str): Destination file.
    """
    path = Path(filename)
    content = json.dumps(data, indent=2) if _is_json(path) else yaml.dump(data)
    path.write_text(content, encoding="utf-8")


def read_dictionary(filename: str, fail_if_missing=True) -> dict:
    """
    Reads a dictionary from a JSON or YAML file.

    Args:
        filename (str): File to read.

    Returns:
        dict: Parsed dictionary (empty if file does not exist).
    """
    path = Path(filename)
    if not path.exists():
        if fail_if_missing:
            raise ValueError(f"{filename=} does not exist")

        return {}

    content = path.read_text(encoding="utf-8")
    return json.loads(content) if _is_json(path) else yaml.safe_load(content)


def save_secret(
    key: str, value: str, password: bytes = None, secrets_file=FILE_SECRETS_DEFAULT
):
    """
    Adds a secret to the encrypted secrets file.

    Args:
        key (str): Identifier for the secret.
        value (str): Value to store.
        password (bytes, optional): Encryption password. Defaults to master password.
        secrets_file (str): Path to the secrets file.
    """
    logger.debug(f"Storing secret: {key}")
    password = password or get_password()

    data = read_dictionary(secrets_file, fail_if_missing=False)
    data[key] = encrypt(value, password)

    store_dictionary(data, secrets_file)
    logger.debug(f"Secret '{key}' saved")


def get_secret(
    key: str,
    password: bytes = None,
    encoding="utf-8",
    secrets_file=FILE_SECRETS_DEFAULT,
):
    """
    Retrieves a secret from the encrypted secrets file.

    Args:
        key (str): Identifier of the secret.
        password (bytes, optional): Decryption password. Defaults to master password.
        encoding (str, optional): Encoding for the decrypted value. Defaults to "utf-8".
        secrets_file (str): Path to the secrets file.

    Returns:
        str | bytes: The decrypted value.

    Raises:
        ValueError: If the secret key is not found.
    """
    logger.debug(f"Retrieving secret: {key}")
    password = password or get_password()

    data = read_dictionary(secrets_file)
    if key not in data:
        raise ValueError(f"Secret '{key}' not found in {secrets_file}")

    return decrypt(data[key], password, encoding)
