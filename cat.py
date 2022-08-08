from pathlib import Path
import click
from typing import List

from oscal.oscal import Metadata, BackMatter, Resource, oscalize_control_id, control_to_sort_order, Role, Property, Link, OSCAL_VERSION
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
            references = c.get("references") if c.get("references") else []
            for r in references:
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

    def add_roles(self, roles_list:List):
        roles:List = [Role]
        for r in roles_list:
            roles.append(Role(
                id=r.get("id"),
                title=r.get("title"),
            ))
        return roles

    def controls(self):
        controls:dict = {}
        for i, c in self.catalog_yaml.items():
            controls[i] = self.add_control(c)
        return controls

    def add_control(self, control:dict):
        """

        """
        references = control.get("references") if control.get("references") else []
        related = control.get("related") if control.get("related") else []

        props = self.add_control_props(control.get("control_number"))
        links = self.get_links(ref=references, rel=related)
        return {"props": props, "links": links}

    def get_links(self, ref:List, rel:List):
        links:List = [Link]
        for rf in ref:
            if rf in self.resource_lookup:
                uuid = self.resource_lookup[rf].uuid
                links.append(Link(
                    href=f"#{uuid}",
                    rel="reference",
                ))

        for rl in rel:
            l = rl.lower()
            links.append(Link(
                href=f"#{l}",
                rel="related",
            ))
        return links

    def add_control_props(self, control_id):
        props:List = [Property]
        props.append(Property(
            name="label",
            value=control_id
        ))
        props.append(Property(
            name="sort-id",
            value=control_to_sort_order(control_id)
        ))
        return props


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

    roles = cat.add_roles([
        {"id": "maintainer", "title": "Document creator"},
        {"id": "system-owner-poc-management", "title": "Contact"},
    ]),
    md = Metadata(
        title="CMS ARS 3.1",
        version=OSCAL_VERSION,
        # roles=roles,
    )
    bm = cat.add_back_matter()
    groups = cat.add_groups()
    controls = cat.controls()
    print(controls)


if __name__ == "__main__":
    main()