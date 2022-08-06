from enum import Enum
from gettext import Catalog
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4
from oscal.oscal import Metadata, OSCALElement, Parameter, Property, BackMatter
from oscal.control import Control

from pydantic import Field

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