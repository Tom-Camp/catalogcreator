from pathlib import Path
import click

from oscal.oscal import Metadata, oscalize_control_id
from ruamel.yaml import YAML

@click.command()
@click.argument(
    "source",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
)
def main(source):
    """
    :param str source: path to YAML file
    """
    file_path = Path(source)
    yaml = YAML(typ="safe")

    with open(file_path, "r+") as y:
        catalog_data = yaml.load(y)

    print(catalog_data)


if __name__ == "__main__":
    main()