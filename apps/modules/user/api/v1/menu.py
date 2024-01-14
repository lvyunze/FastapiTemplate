from fastapi import APIRouter, Depends
from sqlalchemy import select

from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Menu
from apps.modules.user.schemas import GetPageParams, GetParams
from apps.modules.user.schemas.menu import MenuSer
from apps.utils.pagination import Pagination

# 创建路由
router = APIRouter(tags=["菜单管理"])

@router.post('/addOne', summary="添加菜单")
async def addOne(menu: MenuSer):
    """
    添加菜单
    Args:
        menu: 菜单信息
    Returns: 添加结果
    """
    async with db_connect.async_session() as session:
        menu = Menu(**menu.dict())
        session.add(menu)
        await session.commit()
        await session.refresh(menu)
        # 返回添加的菜单信息
        data = MenuSer.dump(menu)
        resp = {
            'code': 200,
            "message": "添加菜单成功",
            "data": data
        }
        return resp

@router.post('/deleteById/<string:id>', summary="删除菜单")
async def deleteById(id):
    """
    删除菜单
    Args:
        id: 菜单id
    Returns: 删除结果
    """
    async with db_connect.async_session() as session:
        # 删除菜单
        await session.execute(select(Menu).where(Menu.id == id).delete())
        resp = {
            'code': 200,
            "message": "菜单删除成功",
            "data": {}
        }
        return resp

@router.post('/updateById/<string:id>', summary="更新菜单")
async def updateById(id,menu: MenuSer):
    """
    更新菜单
    Args:
        menu: 菜单信息
    Returns: 更新结果
    """
    async with db_connect.async_session() as session:
        menu = Menu(**menu.dict())
        menu.id = id
        # 更新menu
        await session.merge(menu)
        resp = {
            'code': 200,
            "message": "菜单修改成功",
            "data": {}
        }
        return resp

@router.get('/findById/<string:id>', summary="根据id查询菜单")
async def findById(id):
    """
    根据id查询菜单
    Args:
        id: 菜单id
    Returns: 菜单信息
    """
    async with db_connect.async_session() as session:
        menu = await session.get(Menu, id)
        data = MenuSer.dump(menu)
        resp = {
            'code': 200,
            "message": "获取菜单信息成功",
            "data": data
        }
        return resp

@router.get('/findList', summary="分页查询菜单列表")
async def findList(params: GetPageParams=Depends()):
    """
    分页查询菜单列表
    Returns: 菜单列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Menu).get_page(session)
        menuList = page_data['list']
        menuList = MenuSer.dump(menuList, many=True)
        total = page_data['total']
        resp = {
            'code': 200,
            "message": "获取菜单列表成功",
            "data": {
                "menuList": menuList,
                "total": total
            }
        }
        return resp

@router.get('/findAll', summary="查询所有菜单")
async def findAll(params: GetParams=Depends()):
    """
    查询所有菜单
    Returns: 菜单列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Menu, all=True).get_page(session)
        menuList = page_data['list']
        menuList = MenuSer.dump(menuList, many=True)
        resp = {
            'code': 200,
            "message": "获取菜单列表成功",
            "data": menuList
        }
        return resp