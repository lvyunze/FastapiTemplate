from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GetPageParams(BaseModel):
    """
    获取分页查询列表参数
    """
    page: int = 1
    pageSize: int = 10
    sortField: Optional[str] = None
    sortOrder: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    keywords: Optional[str] = None
    relations: Optional[str] = None

class GetParams(BaseModel):
    """
    获取全部查询列表参数
    """
    sortField: Optional[str] = None
    sortOrder: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    keywords: Optional[str] = None
    relations: Optional[str] = None