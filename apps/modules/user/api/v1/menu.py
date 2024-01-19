from fastapi import APIRouter, Depends
from sqlalchemy import select

from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Menu
from apps.modules.user.schemas import GetPageParams, GetParams
from apps.modules.user.schemas.menu import MenuSer, GetMenu
from apps.utils.crud import setDefaultData
from apps.utils.pagination import Pagination
from apps.utils.response import Resp
from apps.utils.security import get_current_user_id

# 创建路由
router = APIRouter(tags=["菜单管理"])


@router.post('/addOne', summary="添加菜单", response_model=Resp)
async def addOne(menu: GetMenu, current_user_id: str = Depends(get_current_user_id)):
    """
    添加菜单
    Args:
        menu: 菜单信息
    Returns: 添加结果
    """
    async with db_connect.async_session() as session:
        menu = Menu(**menu.dict())
        setDefaultData(menu, current_user_id)
        session.add(menu)
        await session.commit()
        await session.refresh(menu)
        # 返回添加的菜单信息
        menuSer = MenuSer.dump(menu)

        return Resp(data=menuSer, message="添加菜单成功")


@router.post('/deleteById/{id}', summary="删除菜单", response_model=Resp)
async def deleteById(id: str):
    """
    删除菜单
    Args:
        id: 菜单id
    Returns: 删除结果
    """
    async with db_connect.async_session() as session:
        # 删除菜单
        await session.execute(select(Menu).where(Menu.id == id).delete())

        return Resp(message="删除菜单成功")


@router.post('/updateById/{id}', summary="更新菜单", response_model=Resp)
async def updateById(id: str, menu: MenuSer, current_user_id: str = Depends(get_current_user_id)):
    """
    更新菜单
    Args:
        menu: 菜单信息
    Returns: 更新结果
    """
    async with db_connect.async_session() as session:
        menu = Menu(**menu.dict())
        menu.id = id
        setDefaultData(menu, current_user_id)
        # 更新menu
        await session.merge(menu)

        return Resp(message="更新菜单成功")


@router.get('/findById/{id}', summary="根据id查询菜单", response_model=Resp)
async def findById(id: str):
    """
    根据id查询菜单
    Args:
        id: 菜单id
    Returns: 菜单信息
    """
    async with db_connect.async_session() as session:
        menu = await session.get(Menu, id)
        menuSer = MenuSer.dump(menu)

        return Resp(data=menuSer, message="获取菜单信息成功")


@router.get('/findList', summary="分页查询菜单列表", response_model=Resp)
async def findList(params: GetPageParams = Depends()):
    """
    分页查询菜单列表
    Returns: 菜单列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Menu).get_page(session)
        menuList = page_data['list']
        menuList = MenuSer.dump(menuList, many=True)
        total = page_data['total']

        data = {
            "menuList": menuList,
            "total": total
        }
        return Resp(data=data, message="获取菜单列表成功")


@router.get('/findAll', summary="查询所有菜单", response_model=Resp)
async def findAll(params: GetParams = Depends()):
    """
    查询所有菜单
    Returns: 菜单列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Menu, all=True).get_page(session)
        menuList = page_data['list']
        menuSer = MenuSer.dump(menuList, many=True)

        return Resp(data=menuSer, message="获取菜单列表成功")
