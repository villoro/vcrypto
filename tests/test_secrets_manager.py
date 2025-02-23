from pathlib import Path

import pytest

from vcrypto import secrets_manager as sm
from vcrypto.encryption import create_password

KEY = "secret"
SECRET = "hello"
MDICT = {KEY: SECRET}

FILE_SECRETS_JSON = "temp_secrets.json"
FILE_SECRETS_YAML = "temp_secrets.yaml"
FILE_MASTER_PASSWORD = "test_master.password"
FILE_FAKE = "secrets_imaginary.json"


@pytest.fixture(scope="function", autouse=True)
def cleanup_files():
    """Ensures test files are removed after each test."""
    yield
    for file in [FILE_SECRETS_JSON, FILE_SECRETS_YAML, FILE_MASTER_PASSWORD]:
        Path(file).unlink(missing_ok=True)


def test_get_password(monkeypatch):
    """Test retrieval of a master password from environment and file."""

    # Invalid environment variable
    with pytest.raises(ValueError, match="Password not found"):
        sm.get_password(environ_var_name="IMAGINARY_ENV_VAR")

    # Invalid file
    with pytest.raises(ValueError, match="Password not found"):
        sm.get_password(filename="imaginary_file.password")

    # Retrieve from file
    create_password(filename=FILE_MASTER_PASSWORD)
    assert isinstance(sm.get_password(filename=FILE_MASTER_PASSWORD), bytes)

    # Retrieve from environment variable
    monkeypatch.setenv("SECRET_TEST", "dummy_password")
    assert sm.get_password(environ_var_name="SECRET_TEST") == b"dummy_password"


def test_dictionaries():
    """Test read/write operations for dictionaries (JSON & YAML)."""

    # Test correct reading of JSON
    sm.store_dictionary(MDICT, FILE_SECRETS_JSON)
    assert sm.read_dictionary(FILE_SECRETS_JSON) == MDICT

    # Test correct reading of YAML
    sm.store_dictionary(MDICT, FILE_SECRETS_YAML)
    assert sm.read_dictionary(FILE_SECRETS_YAML) == MDICT


def test_read_write():
    """Test storing and retrieving secrets."""
    password = create_password(store_secret=False)

    # Ensure the file does not exist before testing
    Path(FILE_SECRETS_JSON).unlink(missing_ok=True)

    with pytest.raises(
        ValueError, match=f"filename='{FILE_SECRETS_JSON}' does not exist"
    ):
        sm.read_dictionary(FILE_SECRETS_JSON)

    sm.save_secret(KEY, SECRET, password=password, secrets_file=FILE_SECRETS_JSON)

    assert sm.read_dictionary(FILE_SECRETS_JSON) == {KEY: sm.encrypt(SECRET, password)}
    assert (
        sm.get_secret(KEY, password=password, secrets_file=FILE_SECRETS_JSON) == SECRET
    )


def test_reading_errors():
    """Test handling of missing secrets file."""

    with pytest.raises(ValueError, match=f"filename='{FILE_FAKE}' does not exist"):
        sm.read_dictionary(FILE_FAKE)
