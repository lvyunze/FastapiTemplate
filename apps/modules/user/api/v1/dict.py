# 创建路由
from fastapi import APIRouter, Depends
from sqlalchemy import select

from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Dict
from apps.modules.user.schemas import GetPageParams, GetParams
from apps.modules.user.schemas.dict import GetDict, DictSer
from apps.utils.pagination import Pagination

router = APIRouter(tags=["字典管理"])

@router.post('/addOne', summary="添加字典")
async def addOne(_dict: GetDict):
    """
    添加字典
    Args:
        _dict: 字典信息
    Returns: 添加结果
    """
    async with db_connect.async_session() as session:
        _dict = Dict(**_dict.dict())
        session.add(_dict)
        resp = {
            'code': 200,
            "message": "添加字典信息成功",
            "data": {}
        }
        return resp

@router.post('/deleteById/<string:id>', summary="删除字典")
async def deleteById(id):
    """
    删除字典
    Args:
        id: 字典id
    Returns: 删除结果
    """
    async with db_connect.async_session() as session:
        # 删除字典
        await session.execute(select(Dict).where(Dict.id == id).delete())
        resp = {
            'code': 200,
            "message": "删除字典信息成功",
            "data": {}
        }
        return resp


@router.post('/updateById/<string:id>', summary="更新字典")
async def updateById(id, _dict: GetDict):
    """
    更新字典
    Args:
        _dict: 字典信息
    Returns: 更新结果
    """
    async with db_connect.async_session() as session:
        _dict = Dict(**_dict.dict())
        _dict.id = id
        session.merge(_dict)
        resp = {
            'code': 200,
            "message": "更新字典信息成功",
            "data": {}
        }
        return resp

@router.get('/findById/<string:id>', summary="查询字典")
async def findById(id):
    """
    查询字典
    Args:
        id: 字典id
    Returns: 查询结果
    """
    async with db_connect.async_session() as session:
        dict = await session.get(Dict, id)
        data = DictSer.dump(dict)
        resp = {
            'code': 200,
            "message": "字典信息查询成功",
            "data": data
        }
        return resp

@router.get('/findList', summary="分页查询字典列表")
async def findList(params: GetPageParams=Depends()):
    """
    分页查询字典列表
    Args:
        page: 页码
        size: 每页条数
    Returns: 字典列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Dict).get_page(session)
        dictList = page_data['list']
        dictList = DictSer.dump(dictList, many=True)
        total = page_data['total']
        resp = {
            'code': 200,
            "message": "获取字典信息列表成功",
            "data": {
                "dictList": dictList,
                "total": total
            }
        }
        return resp

@router.get('/findAll', summary="查询所有字典")
async def findAll(params: GetParams=Depends()):
    """
    查询所有字典
    Returns: 所有字典
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Dict, all=True).get_page(session)
        dictList = page_data['list']
        dictList = DictSer.dump(dictList, many=True)
        resp = {
            'code': 200,
            "message": "获取字典信息列表成功",
            "data": {
                "dictList": dictList,
            }
        }
        return resp