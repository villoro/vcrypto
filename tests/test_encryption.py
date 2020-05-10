import pytest

from vcrypto.encryption import create_password, encrypt, decrypt


def test_store_secret():
    """ Test password creation with storing """

    assert create_password(filename="temp.password") is not None

def test_encrypt():
    """ Test that is able to encrypt a secret """

    password = create_password(store_secret=False)
    encrypt("my_secret", password)

def test_decrypt():
    """ Test that by encrypting and decrypting the string is not modified """

    password = create_password(store_secret=False)
    secret = encrypt("my_secret", password)

    assert decrypt(secret, password) == "my_secret"
