from fastapi import APIRouter, Depends
from sqlalchemy import select

from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Atom, RoleAtom, MenuAtom
from apps.modules.user.schemas import GetPageParams, GetParams
from apps.modules.user.schemas.atom import GetAtom, AtomSer
from apps.utils.pagination import Pagination

# 创建路由
router = APIRouter(tags=["原子管理"])

@router.post('/add', summary="添加原子")
async def add(_atom: GetAtom):
    """
    添加原子
    Returns: 添加结果
    """
    _atom = _atom.dict()
    roleIds = _atom.pop("roleIds")
    menuIds = _atom.pop("menuIds")
    async with db_connect.async_session() as session:
        atom = Atom(**_atom)
        session.add(atom)
        await session.commit()
        await session.refresh(atom)
        # 添加原子角色关联
        if roleIds:
            for roleId in roleIds:
                atomRole = RoleAtom(atom_id=atom.id, role_id=roleId, create_user='', update_user='')
                session.add(atomRole)
        # 添加原子菜单关联
        if menuIds:
            for menuId in menuIds:
                atomMenu = MenuAtom(atom_id=atom.id, menu_id=menuId, create_user='', update_user='')
                session.add(atomMenu)
        resp = {
            'code': 200,
            "message": "原子控制添加成功",
            "data": {}
        }
        return resp

@router.post('/deleteById/<string:id>', summary="删除原子")
async def deleteById(id):
    """
    删除原子
    Args:
        id: 原子id
    Returns: 删除结果
    """
    async with db_connect.async_session() as session:
        # 删除原子角色关联
        await session.execute(select(RoleAtom).where(RoleAtom.atom_id == id).delete())
        # 删除原子菜单关联
        await session.execute(select(MenuAtom).where(MenuAtom.atom_id == id).delete())
        # 删除原子
        await session.execute(select(Atom).where(Atom.id == id).delete())
        resp = {
            'code': 200,
            "message": "原子控制删除成功",
            "data": {}
        }
        return resp

@router.post('/updateById/<string:id>', summary="更新原子")
async def updateById(id, _atom: GetAtom):
    """
    更新原子
    Args:
        id: 原子id
        _atom: 原子信息
    Returns: 更新结果
    """
    _atom = _atom.dict()
    roleIds = _atom.pop("roleIds")
    menuIds = _atom.pop("menuIds")
    async with db_connect.async_session() as session:
        # 更新原子
        await session.execute(select(Atom).where(Atom.id == id).update(_atom))

        # 更新原子角色关联
        if roleIds is not None:
            # 删除原子角色关联
            await session.execute(select(RoleAtom).where(RoleAtom.atom_id == id).delete())
            # 添加原子角色关联
            for roleId in roleIds:
                atomRole = RoleAtom(atom_id=id, role_id=roleId, create_user='', update_user='')
                session.add(atomRole)

        # 更新原子菜单关联
        if menuIds is not None:
            # 删除原子菜单关联
            await session.execute(select(MenuAtom).where(MenuAtom.atom_id == id).delete())
            # 添加原子菜单关联
            for menuId in menuIds:
                atomMenu = MenuAtom(atom_id=id, menu_id=menuId, create_user='', update_user='')
                session.add(atomMenu)
        resp = {
            'code': 200,
            "message": "原子按钮修改成功",
            "data": {}
        }
        return resp

@router.get('/findById/<string:id>', summary="根据id查询原子")
async def findById(id):
    """
    根据id查询原子
    Args:
        id: 原子id
    Returns: 原子信息
    """
    async with db_connect.async_session() as session:
        # 查询原子
        atom = await session.get(Atom, id)
        data = AtomSer.dump(atom)
        resp = {
            'code': 200,
            "message": "原子按钮查询成功",
            "data": data
        }
        return resp

@router.get('/findList', summary="分页查询原子列表")
async def findList(params: GetPageParams=Depends()):
    """
    分页查询原子列表
    Args:
        page: 页码
        size: 每页条数
    Returns: 原子列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Atom).get_page(session)
        atomList = page_data['list']
        atomList = AtomSer.dump(atomList, many=True)
        total = page_data['total']
        resp = {
            'code': 200,
            "message": "获取原子列表成功",
            "data": {
                "atomList": atomList,
                "total": total
            }
        }
        return resp

@router.get('/findAll', summary="查询所有原子")
async def findAll(params: GetParams=Depends()):
    """
    查询所有原子
    Returns: 所有原子
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Atom, all=True).get_page(session)
        atomList = page_data['list']
        atomList = AtomSer.dump(atomList, many=True)
        resp = {
            'code': 200,
            "message": "获取菜单列表成功",
            "data": atomList
        }
        return resp