from typing import Iterable, Optional

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select


class Pagination:
    """
    分页器，用于分页查询
    """

    def __init__(self, query_model: BaseModel, model, all=False):
        """
        Args:
            query_model: 查询参数模型
            model: 查询的模型
            all: 是否查询所有数据
        """
        self.model = model
        self.query_model = query_model
        params = self.query_model.dict()
        self.query_params = params  # 查询参数
        self.page = params.get('page')  # 当前页码
        self.pageSize = params.get('pageSize')  # 每页数据量
        self.sortField = params.get('sortField')  # 排序字段
        self.sortOrder = params.get('sortOrder')  # 排序方式
        self.startDate = params.get('startDate')  # 开始时间
        self.endDate = params.get('endDate')  # 结束时间
        self.keywords = params.get('keywords')  # 模糊查询关键字,搞不懂传的是什么，字段？查询内容？
        self.all = all  # 是否查询所有数据

    async def paginate_query(
            self, query: Select, session: AsyncSession
    ) -> Optional[Iterable]:
        """
        返回分页数据
        """

        # 总数据数
        count_statement = select(func.count()).select_from(self.model)
        if query.whereclause is not None:
            count_statement = count_statement.where(query.whereclause)
        count_result = await session.execute(count_statement)
        count = count_result.scalar()
        # 不是查询所有数据，就分页
        if not self.all:
            query = query.limit(self.pageSize).offset((self.page - 1) * self.pageSize)
        # 分页数据
        query_result = await session.execute(query)
        objects = query_result.scalars()

        return {
            'total': count,
            'list': list(objects)
        }

    def get_queryset(self):
        """
        通过类实例化参数query_model生成sql语句
        :return:
        """
        query = select(self.model)

        # 筛选时间段
        if self.startDate:
            query = query.where(getattr(self.model, 'create_time') >= self.startDate)
        if self.endDate:
            query = query.where(getattr(self.model, 'create_time') <= self.endDate)

        # 排序
        if self.sortField:
            if self.sortOrder and self.sortField == 'desc':
                query = query.order_by(getattr(self.model, self.sortField).desc())
            else:
                query = query.order_by(getattr(self.model, self.sortField).asc())

        return query

    async def get_page(self, session: AsyncSession):
        """
        分页器的最顶层方法，不自定义sql语句，可以直接调用page获取页面数据
        :param session:
        :return: dict 包含数据的字典，总数
        """
        query = self.get_queryset()

        return await self.paginate_query(query, session)
