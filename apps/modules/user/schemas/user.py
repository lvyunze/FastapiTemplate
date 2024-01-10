from pydantic import BaseModel, validator
from datetime import datetime
from apps.utils.validate import datetime2timestamp
from apps.ext.sqlalchemy.model import User
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
    dt = validator("update_time", allow_reuse=True)(
        datetime2timestamp
    )

    @validator("username")
    def update_user(cls, v):
        return str(v) + "_"

