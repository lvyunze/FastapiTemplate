from datetime import timezone

from fastapi import APIRouter, Depends
from fastapi_extend import PageNumberPagination, model2schema
from sqlalchemy import select
from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Role, RoleMenu, UserRole
from apps.modules.user.schemas.role import RoleSer, GetRoleQr, GetRole
from apps.response.json_response import resp

# 创建路由
router = APIRouter(tags=["角色管理"])


@router.get('/findById/<string:id>',summary="查询角色")
async def findById(id):
    """
    查询角色
    Args:
        id: 角色id
    Returns: 角色信息
    """
    async with db_connect.async_session() as session:
        role = await session.get(Role, id)
        data = RoleSer.dump(role)
        resp = {
            'code': 200,
            "message": "获取角色信息成功",
            "data": data
        }
        return resp


@router.get('/findList',summary="查询角色列表")
async def findList(params: GetRoleQr = Depends()):
    """
    查询角色列表
    Args:
        params: 查询参数
    Returns: 角色列表
    """
    async with db_connect.async_session() as session:
        paginator = PageNumberPagination(
            params,
            Role,
            RoleSer,
            exclude={"col_id"},
        )
        query = paginator.get_queryset()
        if params.col_id:
            query = query.where(Role.id == params.col_id)
        data = await paginator.paginate_query(query, session)
        resp = {
            'code': 200,
            "message": "获取角色列表成功",
            "data": {
                "roleList": data["list"],
                "total": data["total"]
            }
        }
        return resp

@router.get('/findAll',summary="查询所有角色")
async def findAll():
    """
    查询所有角色
    Returns: 所有角色
    """
    async with db_connect.async_session() as session:
        query = select(Role)
        query_result = await session.execute(query)
        objects = query_result.scalars()
        data = RoleSer.dump(objects, many=True)
        resp = {
            'code': 200,
            "message": "获取角色全部信息成功",
            "data": {
                "roleList": data
            }
        }
        return resp

@router.post('/addOne',summary="添加角色")
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
        data = RoleSer.dump(role)
        resp = {
            'code': 200,
            "message": "添加角色成功",
            "data": data
        }
        return resp

@router.post('/updateById/<string:id>',summary="更新角色")
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
        resp = {
            'code': 200,
            "message": "更新角色成功",
            "data": {}
        }
        return resp

@router.post('/deleteRole/<string:id>',summary="删除角色")
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
        resp = {
            'code': 200,
            "message": "删除角色成功",
            "data": {}
        }
        return resp