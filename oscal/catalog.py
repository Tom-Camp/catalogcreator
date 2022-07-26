from enum import Enum
from gettext import Catalog
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4
from oscal.oscal import Metadata, OSCALElement, Parameter
from oscal.control import Control

from pydantic import Field

class Catalog(OSCALElement):
    uuid: UUID = Field(default_factory=uuid4)
    metadata: Metadata
    params: Optional[List[Parameter]]
    props: Optional[List[Property]]
    controls: Optional[List]



class Model(OSCALElement):
    catalog: Catalog