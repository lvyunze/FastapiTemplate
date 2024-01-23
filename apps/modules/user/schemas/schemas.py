from typing import TypeVar
from pydantic import validator
from apps.utils.serializer import model2schema

T = TypeVar('T')


class GetSer(model2schema(T, exclude=["id"])):
    pass


class SysthemeSer(model2schema(T)):
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)
