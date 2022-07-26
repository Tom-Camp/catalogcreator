

from msilib.schema import Property
from oscal.oscal import OSCALElement, oscalize_control_id

from oscal.oscal import OSCALElement, Link, Parameter, Property
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

class Control(OSCALElement):
    id: str
    title: str
    params: Optional[List[Parameter]]
    props: Optional[List[Property]]
    links: Optional[List[Link]]
    parts: Optional[List[Part]]
    