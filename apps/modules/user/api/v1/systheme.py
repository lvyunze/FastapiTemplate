from fastapi import APIRouter, Depends
from sqlalchemy import select

from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Systheme
from apps.modules.user.schemas import GetPageParams
from apps.modules.user.schemas.systheme import GetSystheme, SysthemeSer
from apps.utils.pagination import Pagination
from apps.utils.response import Resp

# 创建路由
router = APIRouter(tags=["主题管理"])

@router.post('/addOne', summary="添加主题", response_model=Resp)
async def addOne(_systheme: GetSystheme):
    """
    添加主题
    Args:
        systheme: 主题信息
    Returns: 添加结果
    """
    async with db_connect.async_session() as session:
        systheme = Systheme(**_systheme.dict())
        session.add(systheme)

        return Resp(message="添加主题成功")

@router.post('/deleteById/<string:id>', summary="删除主题", response_model=Resp)
async def deleteById(id):
    """
    删除主题
    Args:
        id: 主题id
    Returns: 删除结果
    """
    async with db_connect.async_session() as session:
        # 删除主题
        await session.execute(select(Systheme).where(Systheme.id == id).delete())

        return Resp(message="删除主题成功")

@router.post('/updateById/<string:id>', summary="更新主题", response_model=Resp)
async def updateById(id,_systheme: GetSystheme):
    """
    更新主题
    Args:
        systheme: 主题信息
    Returns: 更新结果
    """
    async with db_connect.async_session() as session:
        systheme = Systheme(**_systheme.dict())
        systheme.id = id
        # 更新systheme
        await session.merge(systheme)
        systhemeSer = SysthemeSer.dump(systheme)

        return Resp(data=systhemeSer, message="更新主题成功")

@router.get('/findById/<string:id>', summary="根据id查询主题", response_model=Resp)
async def findById(id):
    """
    根据id查询主题
    Args:
        id: 主题id
    Returns: 查询结果
    """
    async with db_connect.async_session() as session:
        # 查询主题
        systheme = await session.get(Systheme, id)
        systhemeSer = SysthemeSer.dump(systheme)

        return Resp(data=systhemeSer, message="查询主题成功")

@router.get('/findList', summary="分页查询主题列表", response_model=Resp)
async def findList(params: GetPageParams=Depends()):
    """
    分页查询主题列表
    Returns: 主题列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Systheme).get_page(session)
        systhemeList = page_data['list']
        systhemeList = SysthemeSer.dump(systhemeList, many=True)
        total = page_data['total']

        data = {
            "systhemeList": systhemeList,
            "total": total
        }
        return Resp(data=data, message="分页查询主题列表成功")

@router.get('/findAll', summary="查询所有主题", response_model=Resp)
async def findAll(params: GetPageParams=Depends()):
    """
    查询所有主题
    Returns: 所有主题
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Systheme, all=True).get_page(session)
        systhemeList = page_data['list']
        systhemeList = SysthemeSer.dump(systhemeList, many=True)

        data = {
            "systhemeList": systhemeList,
        }
        return Resp(data=data, message="查询所有主题成功")