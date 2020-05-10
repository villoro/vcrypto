# Palette Material Design
[![Build Status](https://travis-ci.com/villoro/v-crypt.svg?branch=master)](https://travis-ci.com/villoro/v-crypt)

Utility to easily store password/secrets. It uses `Fernet` from the [cryptography](https://cryptography.io/en/latest/) module instead of reinventing the wheel.

Fernet is a symmetric encryption that uses 128-bit AES in CBC mode and PKCS7 padding with HMAC using SHA256 for authentication. You can read more about it [here](https://medium.com/coinmonks/if-youre-struggling-picking-a-crypto-suite-fernet-may-be-the-answer-95196c0fec4b).

## Why v-crypt?
It is always annoying to deal with secrets and passwords in python especially if you work with other people. What we found that worked best for us was:

* Create one master private password (ignored from git)
* Have dict-like file with the rest of passwords encrypted

This module provides the class `Cipher` to handle that easily.

The idea behind this module is to be able to **create a `json` or `yaml` with encrypted secrets**. The keys will be public but the values won't. This way you can **store the dictionary of secrets in git** and easily share them with other people working in the same project. You will only need to **share the `master.password` once**. And all the other passwords/secrets will be tracked with git.

## Installation

You can install it with pip by running:

    pip install v-crypt

## Usage

```python
from v_crypt import Cipher

# Create a cipher instance
cipher = Cipher()

# Create a new master password
cipher.create_password()

# Store a secret
cipher.save_secret("secret", "I like python")

# Retrive a secret
cipher.get_secret("secret")
```

### Customization

There are three paramaters to customize the cipher:

1. **secrets_file:** path of the file with secrets. Can be a `json` or `yaml`.
2. **filename_master_password:** path of the file with the master password
3. **environ_var_name:** if passed it allows to read the master password from an environ var.

> For `yaml` you need to install `pyyaml`

For example you could do:

```python
cipher = Cipher(secrets_file="data/secrets.yaml", filename_master_password="data/master.secret")
```

This will allow you to store both the `master.password` and `secrets.yaml` in the folder `data`.

There is not much more customization since the idea is to keep it simple.

### Integrating it in other projects
We usually have one or more python files with utilities, for example `utilities.py`.

To use v_crypt we initiallize the `cipher` there and then create a `get_secret` dummy function that will call the cipher.

```python
from v_crypt import Cipher

cipher = Cipher(secrets_file="data/secrets.yaml", filename_master_password="data/master.secret")

def get_secret(key):
    return cipher.get_secret(key)
```

Then you can use it elsewhere with:

```python
import utilities as u

u.get_secret("secret")
```

## Development

This package relies on [poetry](https://villoro.com/post/poetry) and `pre-commit`. In order to develop you need to install both libraries with:

```sh
pip install poetry pre-commit
poetry install
pre-commit install
```

Then you need to add `poetry run` before any python shell command. For example:

```sh
# DO
poetry run python master.py

# don't do
python master.py
```

## Authors
* [Arnau Villoro](https://villoro.com)

## License
The content of this repository is licensed under a [MIT](https://opensource.org/licenses/MIT).

## Nomenclature
Branches and commits use some prefixes to keep everything better organized.

### Branches
* **f/:** features
* **r/:** releases
* **h/:** hotfixs

### Commits
* **[NEW]** new features
* **[FIX]** fixes
* **[REF]** refactors
* **[PYL]** [pylint](https://www.pylint.org/) improvements
* **[TST]** tests
