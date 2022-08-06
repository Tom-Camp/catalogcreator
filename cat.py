from pathlib import Path
import click
from typing import List

from oscal.oscal import Metadata, BackMatter, Resource, oscalize_control_id
from oscal.catalog import Group, Catalog
from ruamel.yaml import YAML


class CatMaker:
    def __init__(self, path):
        yaml = YAML(typ="safe")
        with open(path, "r+") as f:
            self.catalog_yaml = yaml.load(f)

    def add_back_matter(self):
        self.backmatter = BackMatter(
            resources=[]
        )
        self.create_resources()
        return self.backmatter
    def create_resources(self):
        self.resource_lookup:dict = {}
        for _, c in self.catalog_yaml.items():
            resources = c.get("references")
            for r in resources:
                if not hasattr(self.resource_lookup, r):
                    rs = Resource(
                        title=r
                    )
                    self.resource_lookup[r] = rs
                    self.backmatter.resources.append(rs)


    def add_groups(self):
        groups:dict = {}
        for i, c in self.catalog_yaml.items():
            fid = i[:2]
            if not hasattr(groups, fid):
                groups[fid] = Group(
                    id=fid,
                    group_class="CMS ARS 3.1",
                    title=c.get("control_family"),
                    params=[],
                    props=[],
                    links=[],
                    parts=[],
                    groups=[],
                    controls=[],
                )
        return groups


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
    cat = CatMaker(file_path)

    md = Metadata(title="CMS ARS 3.1", version="1.0.4")
    bm = cat.add_back_matter()
    groups = cat.add_groups()
    print(groups)


if __name__ == "__main__":
    main()