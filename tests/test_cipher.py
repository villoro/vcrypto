import pytest

from vcrypto.vcrypto import Cipher


key = "secret"
secret = "hello"

secrets_file = "temp_secrets.json"
master_password = "temp.password"

cipher = Cipher(secrets_file=secrets_file, filename_master_password=master_password)

def test_save_secret():
    """ Test that is able to store a secret """

    cipher.create_password(store_secret=True)
    cipher.save_secret(key, secret)

def test_read_secret():
    """ Test read/write of dictionaries """

    cipher.create_password(store_secret=True)
    cipher.save_secret(key, secret)

    assert secret == cipher.get_secret(key)
