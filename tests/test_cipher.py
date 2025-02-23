from vcrypto.vcrypto import Cipher


secrets_file = "temp_secrets.json"
master_password = "temp.password"

cipher = Cipher(secrets_file=secrets_file, filename_master_password=master_password)


def test_save_secret():
    """Test that is able to store a secret"""

    cipher.create_password(store_secret=True)
    cipher.save_secret("secret", "hello")


def test_read_secret():
    """Test read/write of dictionaries"""

    key = "secret"
    secret = "hello"

    cipher.create_password(store_secret=True)
    cipher.save_secret(key, secret)

    assert secret == cipher.get_secret(key)


def test_read_secret_bytes():
    """Test read/write of dictionaries as bytes"""

    key = "secret"
    secret = b"\x80\x03cgoogle"

    cipher.create_password(store_secret=True)
    cipher.save_secret(key, secret)

    assert secret == cipher.get_secret(key, encoding=None)
