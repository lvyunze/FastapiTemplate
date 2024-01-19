from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select

from apps.ext.sqlalchemy import db_connect
from apps.ext.sqlalchemy.models import Atom, RoleAtom, MenuAtom
from apps.modules.user.schemas import GetPageParams, GetParams
from apps.modules.user.schemas.atom import GetAtom, AtomSer
from apps.utils.crud import setDefaultData
from apps.utils.pagination import Pagination
from apps.utils.response import Resp
from apps.utils.security import get_current_user_id

# 创建路由
router = APIRouter(tags=["原子管理"])


@router.post('/add', summary="添加原子", response_model=Resp)
async def add(_atom: GetAtom, current_user_id: str = Depends(get_current_user_id)):
    """
    添加原子
    Returns: 添加结果
    """
    _atom = _atom.dict()
    roleIds = _atom.pop("roleIds")
    menuIds = _atom.pop("menuIds")
    async with db_connect.async_session() as session:
        atom = Atom(**_atom)
        setDefaultData(atom, current_user_id)
        session.add(atom)
        await session.commit()
        await session.refresh(atom)
        # 添加原子角色关联
        if roleIds:
            for roleId in roleIds:
                atomRole = RoleAtom(atom_id=atom.id, role_id=roleId, create_user=current_user_id,
                                    update_user=current_user_id,
                                    create_time=datetime.now, update_time=datetime.now)
                session.add(atomRole)
        # 添加原子菜单关联
        if menuIds:
            for menuId in menuIds:
                atomMenu = MenuAtom(atom_id=atom.id, menu_id=menuId, create_user=current_user_id,
                                    update_user=current_user_id,
                                    create_time=datetime.now, update_time=datetime.now)
                session.add(atomMenu)

        return Resp(message="添加原子成功")


@router.post('/deleteById/{id}', summary="删除原子", response_model=Resp)
async def deleteById(id: str):
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

        return Resp(message="删除原子成功")


@router.post('/updateById/{id}', summary="更新原子", response_model=Resp)
async def updateById(id: str, _atom: GetAtom, current_user_id: str = Depends(get_current_user_id)):
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

        atom = Atom(**_atom)
        atom.id = id
        setDefaultData(atom, current_user_id)
        session.merge(atom)

        # 更新原子角色关联
        if roleIds is not None:
            # 删除原子角色关联
            await session.execute(select(RoleAtom).where(RoleAtom.atom_id == id).delete())
            # 添加原子角色关联
            for roleId in roleIds:
                atomRole = RoleAtom(atom_id=id, role_id=roleId, create_user=current_user_id,
                                    update_user=current_user_id,
                                    create_time=datetime.now, update_time=datetime.now)
                session.add(atomRole)

        # 更新原子菜单关联
        if menuIds is not None:
            # 删除原子菜单关联
            await session.execute(select(MenuAtom).where(MenuAtom.atom_id == id).delete())
            # 添加原子菜单关联
            for menuId in menuIds:
                atomMenu = MenuAtom(atom_id=id, menu_id=menuId, create_user=current_user_id,
                                    update_user=current_user_id,
                                    create_time=datetime.now, update_time=datetime.now)
                session.add(atomMenu)

        return Resp(message="更新原子成功")


@router.get('/findById/{id}', summary="根据id查询原子", response_model=Resp)
async def findById(id: str):
    """
    根据id查询原子
    Args:
        id: 原子id
    Returns: 原子信息
    """
    async with db_connect.async_session() as session:
        # 查询原子
        atom = await session.get(Atom, id)
        atomSer = AtomSer.dump(atom)

        return Resp(data=atomSer, message="获取原子信息成功")


@router.get('/findList', summary="分页查询原子列表", response_model=Resp)
async def findList(params: GetPageParams = Depends()):
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

        data = {
            "atomList": atomList,
            "total": total
        }
        return Resp(data=data, message="获取原子列表成功")


@router.get('/findAll', summary="查询所有原子", response_model=Resp)
async def findAll(params: GetParams = Depends()):
    """
    查询所有原子
    Returns: 所有原子
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, Atom, all=True).get_page(session)
        atomList = page_data['list']
        atomSer = AtomSer.dump(atomList, many=True)

        return Resp(data=atomSer, message="获取原子全部信息成功")
