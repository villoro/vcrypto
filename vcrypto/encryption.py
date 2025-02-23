from typing import Optional
from typing import Union

from cryptography.fernet import Fernet
from loguru import logger


def create_password(filename="test.password", store_secret: bool = True) -> bytes:
    """
    Creates a new password and stores it in a text file.
    This approach is preferred over allowing users to create their own passwords:
        https://stackoverflow.com/a/55147077/3488853

    Args:
        filename: Name of the file where the master password will be stored.
        store_secret: If True, stores the secret in a file.

    Returns:
        Generated master password as bytes.
    """

    # Create a new key
    key = Fernet.generate_key()

    logger.info("Key generated. Remember to store it in a secure place.")

    if not store_secret:
        return key

    logger.info(f"Storing key to {filename=}. Remember to gitignore this file!")

    with open(filename, "w") as file:
        file.write(key.decode())

    return key


def encrypt(value: Union[str, bytes], password: bytes) -> str:
    """
    Encrypts a string or bytes using Fernet.

    Args:
        value: The data to encrypt (string or bytes).
        password: The password used for encryption (must be bytes).

    Returns:
        The encrypted string.
    """

    if not isinstance(value, bytes):
        value = value.encode()

    return Fernet(password).encrypt(value).decode()


def decrypt(
    value: Union[str, bytes], password: bytes, encoding: Optional[str] = "utf-8"
) -> Union[str, bytes]:
    """
    Decrypts an encrypted string using Fernet.

    Args:
        value: The encrypted data (string or bytes).
        password: The password used for decryption (must be bytes).
        encoding: The encoding to use for decoding bytes (if None, returns bytes).

    Returns:
        The decrypted string or bytes if encoding is None.
    """

    if not isinstance(value, bytes):
        value = value.encode()

    decrypted_bytes = Fernet(password).decrypt(value)

    if encoding:
        return decrypted_bytes.decode(encoding)

    return decrypted_bytes
