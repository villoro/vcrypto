from pathlib import Path

import pytest

from vcrypto.encryption import create_password
from vcrypto.encryption import decrypt
from vcrypto.encryption import encrypt

TEMP_PASSWORD_FILE = "temp.password"


@pytest.fixture(autouse=True)
def cleanup_files():
    """Ensures test files are removed after each test."""
    yield
    Path(TEMP_PASSWORD_FILE).unlink(missing_ok=True)


def test_store_secret():
    """Test password creation with storing"""

    assert create_password(filename=TEMP_PASSWORD_FILE) is not None


def test_create_password_does_not_overwrite():
    """Refuse to overwrite an existing master password file."""

    create_password(filename=TEMP_PASSWORD_FILE)

    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        create_password(filename=TEMP_PASSWORD_FILE)


def test_encrypt():
    """Test that is able to encrypt a secret"""

    password = create_password(store_secret=False)
    encrypt("my_secret", password)


def test_decrypt():
    """Test that by encrypting and decrypting the string is not modified"""

    value = "my_secret"

    password = create_password(store_secret=False)
    secret = encrypt(value, password)

    assert decrypt(secret, password) == value


def test_decrypt_bytes():
    """Test that by encrypting and decrypting bytes is not modified"""

    value = b"\x80\x03cgoogle"

    password = create_password(store_secret=False)
    secret = encrypt(value, password)

    assert decrypt(secret, password, encoding=None) == value


def test_decrypt_latin1():
    """Test that by encrypting and decrypting bytes as latin1 is not modified"""

    password = create_password(store_secret=False)
    secret = encrypt(b"\x80\x03cgoogle", password)

    assert decrypt(secret, password, encoding="latin1") == "\x80\x03cgoogle"
