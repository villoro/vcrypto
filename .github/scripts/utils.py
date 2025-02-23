import os

import toml
from loguru import logger as log

PYPROJECT_FILE = "pyproject.toml"


def read_pyproject():
    return toml.load(PYPROJECT_FILE)


def set_output(name, value):
    log.info(f"Setting {name=} {value=}")
    with open(os.environ["GITHUB_ENV"], "a") as fh:
        print(f"{name}={value}", file=fh)


def get_version_from_toml():
    config = read_pyproject()
    return config["project"]["version"]
