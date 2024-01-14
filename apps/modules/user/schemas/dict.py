from fastapi_extend import model2schema
from pydantic import validator

from apps.ext.sqlalchemy.models import Dict

class GetDict(model2schema(Dict, exclude=["id"])):
    pass

class DictSer(model2schema(Dict)):
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)
    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)