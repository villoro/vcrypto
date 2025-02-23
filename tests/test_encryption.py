from vcrypto.encryption import create_password
from vcrypto.encryption import decrypt
from vcrypto.encryption import encrypt


def test_store_secret():
    """Test password creation with storing"""

    assert create_password(filename="temp.password") is not None


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
