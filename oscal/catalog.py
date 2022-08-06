from __future__ import annotations
from dataclasses import dataclass
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4
from oscal.oscal import Metadata, OSCALElement, Parameter, Property, BackMatter, Link, Part
from oscal.control import Control
from pydantic import Field


class Group(OSCALElement):
    id: Optional[str]
    group_class: Optional[str]
    title: str
    params: Optional[List[Parameter]]
    props: Optional[List[Property]]
    links: Optional[List[Link]]
    parts: Optional[List[Part]]
    groups: Optional[List[Group]]
    controls: Optional[List[Control]]

    class Config:
        fields = {"group_class": "class"}
        allow_population_by_field_name = True


class Catalog(OSCALElement):
    uuid: UUID = Field(default_factory=uuid4)
    metadata: Metadata
    params: Optional[List[Parameter]]
    controls: Optional[List]
    props: Optional[List[Property]]
    back_matter: Optional[BackMatter]

    class Config:
        fields = {"back_matter": "back-matter"}
        allow_population_by_field_name = True


class Model(OSCALElement):
    catalog: Catalog
