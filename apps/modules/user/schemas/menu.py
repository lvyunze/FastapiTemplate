from typing import List
from fastapi_extend import model2schema
from pydantic import validator, Field

from apps.ext.sqlalchemy.models import Menu
from apps.modules.user.schemas.atom import AtomSer


class MenuSer(model2schema(Menu, exclude=["id"])):
    children: List['MenuSer'] = Field(default_factory=list)
    atomList: List[AtomSer] = Field(default_factory=list)
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)
    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)
