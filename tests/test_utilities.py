import os

from vcrypto import utilities as u


key = "secret"
secret = "hello"

mdict = {key: secret}

file_secrets = "temp_secrets.json"


def test_get_password():
    """Test that it is able to retrieve a master password."""

    # Test invalid environ var
    assert u.get_password(environ_var_name="imaginary_env_var") is None

    # Test invalid file
    assert u.get_password(filename="imaginary_file.password") is None

    # Retrieve from file
    u.create_password(filename="test.password")
    assert isinstance(u.get_password(filename="test.password"), bytes)

    # Retrieve from env var
    os.environ["SECRET_TEST"] = "dummy_password"
    assert isinstance(u.get_password(environ_var_name="SECRET_TEST"), bytes)


def test_dictionaries():
    """Test read/write of dictionaries"""

    # Test correct reading of json
    u.store_dictionary(mdict, file_secrets)
    u.read_dictionary(filename="temp.password")

    # Test correct reading of yaml
    u.store_dictionary(mdict, "temp_secrets.yaml")
    u.read_dictionary("temp_secrets.yaml")


def test_read_write():
    """Test that is possible to read and write secrets"""

    password = u.create_password(store_secret=False)

    # Remove if file exists
    if os.path.isfile(file_secrets):
        os.remove(file_secrets)

    # Test it before and after file is created
    u.save_secret(key, secret, password=password, secrets_file=file_secrets)
    u.save_secret(key, secret, password=password, secrets_file=file_secrets)

    assert secret == u.get_secret(key, password=password, secrets_file=file_secrets)


def test_reading_errors():
    """Test that it handles reading errors"""

    password = u.create_password(store_secret=False)

    assert u.get_secret(key, password, secrets_file="secrets_imaginary.json") is None
