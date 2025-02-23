from pathlib import Path

import pytest

from vcrypto import vcrypto

KEY = "test_key"
SECRET = "super_secret"
SECRETS_FILE = "temp_secrets.json"
MASTER_PASSWORD_FILE = "temp_master.password"


@pytest.fixture(scope="function", autouse=True)
def cleanup_files():
    """Ensures test files are removed after each test."""
    yield
    for file in [SECRETS_FILE, MASTER_PASSWORD_FILE]:
        Path(file).unlink(missing_ok=True)


def test_init_vcrypto():
    """Test that Vcrypto initializes properly and enforces singleton behavior."""

    vcrypto.init_vcrypto(SECRETS_FILE, MASTER_PASSWORD_FILE)

    # Ensure Vcrypto is initialized
    assert vcrypto._VCRYPTO is not None
    assert vcrypto._VCRYPTO.secrets_file == SECRETS_FILE
    assert vcrypto._VCRYPTO.filename_master_password == MASTER_PASSWORD_FILE


def test_save_and_get_secret():
    """Test saving and retrieving secrets using global functions."""
    vcrypto.init_vcrypto(SECRETS_FILE, MASTER_PASSWORD_FILE)

    vcrypto.create_password(store_secret=True)  # Generate a master password
    vcrypto.save_secret(KEY, SECRET)

    retrieved_secret = vcrypto.get_secret(KEY)
    assert retrieved_secret == SECRET, "Decrypted secret should match original"
