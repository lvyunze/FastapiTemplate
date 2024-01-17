from datetime import timezone

from fastapi import APIRouter, Depends
from fastapi_extend import PageNumberPagination, model2schema
from sqlalchemy import select
from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Role, RoleMenu, UserRole
from apps.modules.user.schemas import GetPageParams, GetParams
from apps.modules.user.schemas.role import RoleSer, GetRoleQr, GetRole
from apps.response.json_response import resp
from apps.utils.pagination import Pagination
from apps.utils.response import Resp

# 创建路由
router = APIRouter(tags=["角色管理"])


@router.get('/findById/<string:id>',summary="查询角色",response_model=Resp)
async def findById(id):
    """
    查询角色
    Args:
        id: 角色id
    Returns: 角色信息
    """
    async with db_connect.async_session() as session:
        role = await session.get(Role, id)
        roleSer = RoleSer.dump(role)

        return Resp(data=roleSer,message="获取角色信息成功")


@router.get('/findList',summary="查询角色列表",response_model=Resp)
async def findList(params: GetPageParams = Depends()):
    """
    查询角色列表
    Args:
        params: 查询参数
    Returns: 角色列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Role).get_page(session)
        roleList = page_data['list']
        roleList = RoleSer.dump(roleList, many=True)
        total = page_data['total']

        data = {
            "roleList": roleList,
            "total": total
        }
        return Resp(data=data,message="获取角色列表成功")

@router.get('/findAll',summary="查询所有角色",response_model=Resp)
async def findAll(params: GetParams=Depends()):
    """
    查询所有角色
    Returns: 所有角色
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Role, all=True).get_page(session)
        roleList = page_data['list']

        data = {
            "roleList": roleList,
        }
        return Resp(data=data,message="获取角色全部信息成功")

@router.post('/addOne',summary="添加角色",response_model=Resp)
async def addOne(role: GetRole):
    """
    添加角色
    Args:
        role: 角色信息
    Returns: 添加结果
    """
    async with db_connect.async_session() as session:
        role = Role(**role.dict())
        session.add(role)
        await session.commit()
        await session.refresh(role)
        # 返回添加的角色信息
        roleSer = RoleSer.dump(role)

        return Resp(data=roleSer,message="添加角色成功")

@router.post('/updateById/<string:id>',summary="更新角色",response_model=Resp)
async def updateById(id,role: RoleSer):
    """
    更新角色
    Args:
        role: 角色信息
    Returns: 更新结果
    """
    async with db_connect.async_session() as session:
        role = Role(**role.dict())
        role.id = id
        # 更新role
        await session.merge(role)

        return Resp(message="更新角色成功")

@router.post('/deleteRole/<string:id>',summary="删除角色",response_model=Resp)
async def deleteRole(id):
    """
    删除角色
    Args:
        id: 角色id
    Returns: 删除结果
    """
    async with db_connect.async_session() as session:
        # 删除角色菜单关联表
        await session.execute(select(RoleMenu).where(RoleMenu.role_id == id).delete())
        # 删除角色用户关联表
        await session.execute(select(UserRole).where(UserRole.role_id == id).delete())
        # 删除角色
        role = await session.get(Role, id)
        await session.delete(role)

        return Resp(message="删除角色成功")