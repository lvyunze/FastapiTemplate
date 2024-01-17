from typing import Optional, List
from pydantic import BaseModel, validator
from apps.ext.sqlalchemy.models import User
from apps.modules.user.schemas.role import RoleSer
from apps.modules.user.schemas.systheme import SysthemeSer
from apps.utils.serializer import model2schema

class AuthDetails(BaseModel):
    """
    用户登录信息
    """
    username: str
    password: str


class GetUser(BaseModel):
    """
    接收用户查询参数
    """
    col_id: int = None
    username: str = None
    page: int = 1
    pageSize: int = 100
    sort_field: str = 'update_time'
    order_by: str = 'desc'



class UserSer(model2schema(User)):
    """
    用户序列化
    """
    # @validator("username")
    # def update_user(cls, v):
    #     return str(v) + "_"

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

    # @validator("username")
    # def update_user(cls, v):
    #     return str(v) + "_"

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