import click
from loguru import logger
from utils import get_version_from_toml
from utils import set_output


@click.command()
@click.option("--name")
def export_version(name):
    version = get_version_from_toml()
    logger.info(f"'{name}' branch {version=}")

    set_output(f"VERSION_{name.upper()}", version)


if __name__ == "__main__":
    export_version()
