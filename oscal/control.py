from __future__ import annotations
from dataclasses import dataclass
from oscal.oscal import OSCALElement, Link, Parameter, Property, Part
from typing import List
from typing import Optional


class Control(OSCALElement):
    id: str
    control_class: Optional[str]
    title: str
    params: Optional[List[Parameter]]
    props: Optional[List[Property]]
    links: Optional[List[Link]]
    parts: Optional[List[Part]]
    controls: Optional[List[Control]]


    class Config:
        fields = {"control_class": "class"}
        allow_population_by_field_name = True
