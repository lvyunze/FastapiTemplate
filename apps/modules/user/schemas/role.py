from apps.utils.serializer import model2schema
from pydantic import validator, BaseModel
from apps.ext.sqlalchemy.models import Role


class GetRoleQr(BaseModel):
    col_id: int = None
    page: int = 1
    pageSize: int = 10
    sort_field: str = 'update_time'
    order_by: str = 'desc'


class GetRole(model2schema(Role, exclude=["id"])):
    pass


class RoleSer(model2schema(Role)):
    # dt = validator("update_time", allow_reuse=True)(
    #     timestamp2datetime
    # )
    # 日期转为2023-08-21 00:00:00格式
    @validator("update_time", allow_reuse=True)
    def update_time(cls, v):
        return str(v)

    @validator("create_time", allow_reuse=True)
    def create_time(cls, v):
        return str(v)
    pass
