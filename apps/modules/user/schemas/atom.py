from typing import Optional, List
from pydantic import validator

from apps.ext.sqlalchemy.models import Atom
from apps.utils.serializer import model2schema


class GetAtom(model2schema(Atom, exclude=["id"])):
    roleIds: Optional[List[str]] = None
    menuIds: Optional[List[str]] = None

class AtomSer(model2schema(Atom)):
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)
    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)
    pass