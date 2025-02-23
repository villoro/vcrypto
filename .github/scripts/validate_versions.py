import utils
from loguru import logger


def validate_versions():
    version_pyproject = utils.get_version_from_toml("dbt")
    version_dbt = utils.get_version_from_dbt_project()

    logger.info(f"{version_pyproject=} {version_dbt=}")

    raw_message = f"Versions from '{utils.PYPROJECT_FILE}' and '{utils.DBT_PROJECT}'"

    if version_pyproject == version_dbt:
        logger.success(f"{raw_message} match")
        exit(0)

    logger.error(f"{raw_message} don't match")
    exit(1)


if __name__ == "__main__":
    validate_versions()
