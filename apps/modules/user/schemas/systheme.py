from fastapi_extend import model2schema
from pydantic import validator

from apps.ext.sqlalchemy.models import Systheme

class GetSystheme(model2schema(Systheme, exclude=["id"])):
    pass

class SysthemeSer(model2schema(Systheme)):
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)
    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)