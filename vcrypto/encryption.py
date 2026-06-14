import os
from pathlib import Path
from typing import Optional
from typing import Union

from cryptography.fernet import Fernet
from loguru import logger


def write_private_file(filename: str, data: Union[str, bytes]) -> None:
    """
    Writes data to a file readable/writable only by the owner.

    Uses ``os.open`` with mode ``0o600`` so the restrictive permissions are set
    when the file is created, avoiding a window where it is world-readable. On
    POSIX this yields owner-only access; on Windows the mode is largely ignored
    (access is governed by ACLs) but the call remains harmless.

    Args:
        filename: Destination path.
        data: Content to write (str or bytes).
    """

    binary = isinstance(data, bytes)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(filename, flags, 0o600)
    with os.fdopen(fd, "wb" if binary else "w") as file:
        file.write(data)


def create_password(filename="master.password", store_secret: bool = True) -> bytes:
    """
    Creates a new password and stores it in a text file.
    This approach is preferred over allowing users to create their own passwords:
        https://stackoverflow.com/a/55147077/3488853

    Args:
        filename: Name of the file where the master password will be stored.
        store_secret: If True, stores the secret in a file.

    Returns:
        Generated master password as bytes.

    Raises:
        FileExistsError: If the destination file already exists. Overwriting the
            master password would make every secret encrypted with the previous
            key permanently undecryptable, so this must be done deliberately.
    """

    # Create a new key
    key = Fernet.generate_key()

    logger.info("Key generated. Remember to store it in a secure place.")

    if not store_secret:
        return key

    if Path(filename).exists():
        raise FileExistsError(
            f"Refusing to overwrite the existing master password at {filename!r}. "
            "Delete it manually first if you really intend to generate a new key "
            "(every secret encrypted with the old key will become undecryptable)."
        )

    logger.info(f"Storing key to {filename=}. Remember to gitignore this file!")

    write_private_file(filename, key.decode())

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
