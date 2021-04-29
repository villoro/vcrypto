"""
    Utility to storing password/secrets safely.

    You can save a secret using:
        utilities.save_secret("test_key", "my_super_secret_text")

    And then you can retrive it by:
        value = utilities.get_secret("test_key")

    In order to do that you'll need an environ var or a txt with the secret.

    To create a master password:
        utilities.create_password()
"""

import json
import os

from .defaults import FILE_MASTER_DEFAULT
from .defaults import FILE_SECRETS_DEFAULT_JSON
from .encryption import create_password
from .encryption import decrypt
from .encryption import encrypt


def get_password(filename=FILE_MASTER_DEFAULT, environ_var_name=None):
    """
        Retrives master password. By default it is read from a file.
        If can also be retrived from as environment var

        Args:
            filaname:           name of the file with the master password
            environ_var_name:   name of the environ variable where the master password is
    """

    # If there is an environ variable use it instead of reading the file with secret
    if environ_var_name is not None:
        password = os.environ.get(environ_var_name, None)

        if password is None:
            print(f"Environ variable {environ_var_name} does not exist")
            return None

        return password.encode()

    try:
        with open(filename, "r") as file:
            return file.read().replace("\n", "").encode()

    except IOError:
        print(f"File {filename} with secret not found")
        return None


def store_dictionary(data, filename):
    """
        Stores a dictionary in a file. It can store 'json' and 'yaml' files.
        
        Args:
            data:       dictionary to store
            filename:   where to store the dictionary
    """

    extension = filename.split(".")[-1]

    # Store a json file
    if extension == "json":
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)

    # Store a yaml
    if extension in ["yml", "yaml"]:

        # Check that yaml is installed
        try:
            import yaml
        except ImportError:
            raise ImportError("yaml module missing: you migh solve it with 'pip install pyyaml'")

        with open(filename, "w") as file:
            yaml.dump(data, file)


def read_dictionary(filename):
    """ Reads a dictionary. It can read 'json' and 'yaml' files """

    extension = filename.split(".")[-1]

    # Store a json file
    if extension == "json":
        with open(filename, "r") as file:
            return json.load(file)

    # Store a yaml
    if extension in ["yml", "yaml"]:

        # Check that yaml is installed
        try:
            import yaml
        except ImportError:
            raise ImportError("yaml module missing: you migh solve it with 'pip install pyyaml'")

        with open(filename, encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.SafeLoader)


def save_secret(key, value, password=None, secrets_file=FILE_SECRETS_DEFAULT_JSON):
    """
        Add one secret in the json of secrets. It will create the json if needed

        Args:
            key:            id of the secret
            value:          what to store
            password:       password for encryption, if non use SMA secret
            secrets_file:   path of the file with secrets
    """

    if password is None:
        password = get_password()

    # Create an empty dict if file not found
    try:
        data = read_dictionary(secrets_file)

    except FileNotFoundError:
        data = {}

    data[key] = encrypt(value, password)

    store_dictionary(data, secrets_file)

    print(f"Secret '{key}' saved")


def get_secret(key, password=None, encoding="utf8", secrets_file=FILE_SECRETS_DEFAULT_JSON):
    """
        Retrives one secret from the json of secrets

        Args:
            key:            id of the secret
            password:       password for encryption, if non use SMA secret
            encoding:       encoding to use for decoding bytes [if None returns bytes]
            secrets_file:   path of the file with secrets
    """

    if password is None:
        password = get_password()

    # Create an empty dict if file not found
    try:
        data = read_dictionary(secrets_file)

    except FileNotFoundError:
        data = {}

    if key not in data:
        print(f"Key '{key}' not found in {secrets_file}")
        return None

    return decrypt(data[key], password, encoding=encoding)
