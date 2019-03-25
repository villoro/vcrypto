"""
    Utility to storing password/secrets safely.

    You can save a secret using:
        v_crypt.save_secret("test_key", "my_super_secret_text")

    And then you can retrive it by:
        value = v_crypt.get_secret("test_key")

    In order to do that you'll need an environ var or a txt with the secret.
    
    To create a master password:
        v_crypt.create_password()
"""

import io
import json

from cryptography.fernet import Fernet


FILE_SECRET_DEFAULT = "secret.txt"
FILE_SECRETS_DEFAULT = "secrets.json"


def create_password(filename=FILE_SECRET_DEFAULT, store_secret=True):
    """
        Creates a new password and stores the password in a text file

        Args:
            filename:       name of the file where to store the master password
            store_secret:   if true store the secret in a file

        Returns:
            master password
    """

    # Create a new key and transform it to string
    key = Fernet.generate_key()

    print("Key generated. Remember to store it in a secure place.")

    if store_secret:
        with open(filename, "w") as file:
            file.write(key.decode())

        print(f"Key stored in {filename}. Remember to gitignore this file!")

    return key


def _get_password(filename=FILE_SECRET_DEFAULT, environ_var_name=None):
    """
        Retrives master password. By default it is read from a file.
        If can also be retrived from as environment var

        Args:
            filaname:           name of the file with the master password
            environ_var_name:   name of the environ variable where the master password is
    """

    # If there is an environ variable use it instead of reading the file with secret
    if environ_var_name is not None:
        password = os.environ.get(c.io.ENV_VAR_SECRET_NAME, None)

        if password is None:
            print(f"Environ variable {environ_var_name} does not exist")

        return password.encode()

    try:
        with open(filename, "r") as file:
            return file.read().replace("\n", "").encode()

    except IOError:
        print(f"File {filename} with secret not found")
        return None


def _encrypt(value, password):
    """
        Encrypts a string using Fernet

        Args:
            value:      what to encrypt [string]
            password:   password to use [bytes]

        Returns:
            encrypted string
    """

    return Fernet(password).encrypt(value.encode()).decode()


def _decrypt(value, password):
    """
        Encrypts a string using Fernet

        Args:
            value:      what to dencrypt [string]
            password:   password to use [bytes]

        Returns:
            decrypted string
    """

    return Fernet(password).decrypt(value.encode()).decode()


def save_secret(key, value, password=None, secrets_file=FILE_SECRETS_DEFAULT):
    """
        Add one secret in the json of secrets. It will create the json if needed

        Args:
            key:            id of the secret
            value:          what to store
            password:       password for encryption, if non use SMA secret
            secrets_file:   path of the file with secrets
    """

    if password is None:
        password = _get_password()

    try:
        with open(secrets_file, "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        data = {}

    data[key] = _encrypt(value, password)

    with open(secrets_file, "w") as file:
        json.dump(data, file, indent=2)

    print(f"Secret '{key}' saved")


def get_secret(key, password=None, secrets_file=FILE_SECRETS_DEFAULT):
    """
        Retrives one secret from the json of secrets

        Args:
            key:            id of the secret
            password:       password for encryption, if non use SMA secret
            secrets_file:   path of the file with secrets
    """

    if password is None:
        password = _get_password()

    with open(secrets_file, "r") as file:
        data = json.load(file)

    if key not in data:
        print(f"Key '{key}' not found in {secrets_file}")
        return None

    return _decrypt(data[key], password)
