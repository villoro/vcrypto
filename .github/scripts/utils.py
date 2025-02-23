import os
from pathlib import Path

import toml
import yaml
from loguru import logger

PYPROJECT_FILE = "pyproject.toml"
DBT_PROJECT = "dbt_northius/dbt_project.yml"

BASE_PATH = str(Path(__file__).parent.parent.parent / "dbt_northius")
PATH_MODELS = f"{BASE_PATH}/models"


def read_pyproject():
    return toml.load(PYPROJECT_FILE)


def get_aws_config():
    logger.info(f"Reading 'aws-config' from '{PYPROJECT_FILE}'")
    return read_pyproject()["aws-config"]


def set_output(name, value):
    logger.info(f"Setting {name=} {value=}")
    with open(os.environ["GITHUB_ENV"], "a") as fh:
        print(f"{name}={value}", file=fh)


def get_version_from_toml(project="dbt"):
    config = read_pyproject()

    if project == "dbt":
        logger.info("Retrieving dbt/python version")
        aux = config["tool"]["poetry"]
    elif project == "docker":
        logger.info("Retrieving docker version")
        aux = config["docker"]
    else:
        logger.error(f"{project=} must be 'dbt' or 'docker'")

    return aux["version"]


def get_version_from_dbt_project():
    logger.info(f"Retrieving project version from '{DBT_PROJECT}'")

    with open(DBT_PROJECT) as stream:
        data = yaml.safe_load(stream)

    return data["version"]


def save_pyproject(data):
    logger.info(f"Exporting '{PYPROJECT_FILE}'")
    with open(PYPROJECT_FILE, "w", encoding="utf8") as stream:
        toml.dump(data, stream)


def get_all_files(extensions):
    out = []
    for path, _, files in os.walk(PATH_MODELS):
        for file in files:
            if any([file.endswith(f".{x}") for x in extensions]):
                out.append(f"{path}/{file}".replace("\\", "/"))
    return out
