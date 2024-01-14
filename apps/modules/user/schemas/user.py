from typing import Optional, List

from pydantic import BaseModel, validator
from datetime import datetime

from apps.ext.sqlalchemy.models import User
from apps.modules.user.schemas.role import RoleSer
from apps.modules.user.schemas.systheme import SysthemeSer
from apps.utils.validate import datetime2timestamp
# from apps.ext.sqlalchemy.model import User
from fastapi_extend.serializer import model2schema


class AuthDetails(BaseModel):
    username: str
    password: str


class GetUser(BaseModel):
    col_id: int = None
    username: str = None
    page: int = 1
    pageSize: int = 100
    sort_field: str = 'update_time'
    order_by: str = 'desc'



class UserSer(model2schema(User)):

    @validator("username")
    def update_user(cls, v):
        return str(v) + "_"

    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)

class UserListSer(model2schema(User)):
    roleList: List[RoleSer] = []
    roleIds: List[str] = []
    systhemeInfo: Optional[SysthemeSer] = None

    @validator("username")
    def update_user(cls, v):
        return str(v) + "_"

    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)

class UserForm(model2schema(User,exclude=["id","create_time","update_time"])):

    roleIds: Optional[List[str]] = None