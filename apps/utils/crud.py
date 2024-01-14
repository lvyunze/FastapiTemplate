from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def getRelationshipData(session: AsyncSession, source, target, relation=None):
    """
    获取关联数据
    Args:
        session: 数据库连接
        source: 源模型实例
        target: 目标模型类
        relation: 中间模型类
    Returns: 关联数据
    """

    # 获取源模型关联id名
    sourceIdName = source.__tablename__ + "_id"
    # 获取目标模型关联id名
    targetIdName = target.__tablename__ + "_id"

    # 一对一，直接关联
    if relation is None:
        # 查询关联数据
        query_result = await session.execute(select(target).where(getattr(source, targetIdName) == target.id))
        objects = query_result.scalars().first()
        data = objects
        return data
    # 一对多,关联中间表
    else:
        # 关联查询目标模型
        query_result = await session.execute(
            select(target).join(relation, getattr(target, 'id') == getattr(relation, targetIdName))
            .where(getattr(relation, sourceIdName) == source.id))
        objects = query_result.scalars()
        data = list(objects)
        return data
