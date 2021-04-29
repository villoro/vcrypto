"""
    Encrypt/Decrypt functions using Fernet.

    You can encrypt a string with:
        encryption.encrypt("secret", key)

    And then you can decrypt it with:
        value = encryption.decrypt(crypted_string, key)

    In order to do that you'll need an environ var or a txt with the secret.
    
    To create a master password:
        encryption.create_password()
"""

from cryptography.fernet import Fernet

from .defaults import FILE_MASTER_DEFAULT
from .defaults import STORE_SECRET


def create_password(filename=FILE_MASTER_DEFAULT, store_secret=STORE_SECRET):
    """
        Creates a new password and stores the password in a text file.
        It is better than allowing the user to create the password:
            https://stackoverflow.com/a/55147077/3488853

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


def encrypt(value, password):
    """
        Encrypts a string using Fernet

        Args:
            value:      what to encrypt [string/bytes]
            password:   password to use [bytes]

        Returns:
            encrypted string
    """

    if type(value) != bytes:
        value = value.encode()

    return Fernet(password).encrypt(value).decode()


def decrypt(value, password, encoding="utf8"):
    """
        Encrypts a string using Fernet

        Args:
            value:      what to dencrypt [string/bytes]
            password:   password to use [bytes]
            encoding:   encoding to use for decoding bytes [if None returns bytes]

        Returns:
            decrypted string
    """

    if type(value) != bytes:
        value = value.encode()

    out = Fernet(password).decrypt(value)

    if encoding:
        return out.decode(encoding)

    return out
