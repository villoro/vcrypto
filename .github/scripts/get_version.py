import click
from loguru import logger
from utils import get_version_from_toml
from utils import set_output


@click.command()
@click.option("--name")
@click.option("--project", default="dbt", help="'dbt' or 'docker'")
def export_version(name, project):
    version = get_version_from_toml(project)
    logger.info(f"'{name}' branch {version=}")

    set_output(f"VERSION_{name.upper()}", version)


if __name__ == "__main__":
    export_version()
