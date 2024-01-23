from typing import Optional, List
from pydantic import BaseModel, validator, Field
from apps.ext.sqlalchemy.models import User, Systheme, Role, Atom, Menu
from apps.modules.user.schemas.atom import AtomSer
from apps.modules.user.schemas.role import RoleSer
from apps.modules.user.schemas.systheme import SysthemeSer
from apps.utils.serializer import model2schema

class AuthDetails(BaseModel):
    """
    用户登录信息
    """
    username: str
    password: str

class UserRegister(BaseModel):
    """
    用户注册信息
    """
    name: Optional[str] = None
    username: str
    password: str

class GetUser(model2schema(User,exclude=["id"])):
    """
    接收用户查询参数
    """
    roleIds: Optional[List[str]] = None



class UserSer(model2schema(User)):
    """
    用户序列化
    """

    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)
    pass

class UserListSer(model2schema(User)):
    """
    用户序列化
    """
    roleList: List[RoleSer] = []
    roleIds: List[str] = []
    systhemeInfo: Optional[SysthemeSer] = None

    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)

class UserForm(model2schema(User,exclude=["id","create_time","update_time"])):
    """
    用户序列化
    """
    roleIds: Optional[List[str]] = None

class GetSystheme(model2schema(Systheme, exclude=["id"])):
    pass

class SysthemeSer(model2schema(Systheme)):
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)
    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)
    pass

class GetRole(model2schema(Role, exclude=["id"])):
    pass


class RoleSer(model2schema(Role)):
    # 日期转为2023-08-21 00:00:00格式
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)
    pass

class GetMenu(model2schema(Menu, exclude=["id"])):
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)

class MenuSer(model2schema(Menu)):
    children: List['MenuSer'] = Field(default_factory=list)
    atomList: List[AtomSer] = Field(default_factory=list)
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)
    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)

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