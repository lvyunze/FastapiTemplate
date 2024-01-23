from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from apps.ext.sqlalchemy.models import User, Systheme, Menu, RoleMenu, Role, UserRole, Atom, MenuAtom
from apps.modules.user.schemas import GetPageParams, GetParams
from apps.modules.user.schemas.user import UserForm, UserListSer, AuthDetails, GetUser, UserRegister, RoleSer, \
    SysthemeSer, MenuSer
from apps.ext.sqlalchemy import db_connect
from apps.modules.user.schemas.user import UserSer
from fastapi import Depends

from apps.utils.crud import get_relationship_data, set_default_data
from apps.utils.pagination import Pagination
from apps.utils.response import Resp
from apps.utils.security import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, \
    Token, get_current_user_id, get_password_hash

router = APIRouter(tags=["用户管理"])


@router.post('/login', summary="用户登录", response_model=Resp)
async def login(auth_details: AuthDetails):
    """
    用户登录
    Args:
        auth_details: 用户登录信息
    Returns: 登录结果
    """
    # print(f"{auth_details.username}/{auth_details.password}")
    async with db_connect.async_session() as session:
        # 判断用户是否存在
        user = await authenticate_user(session, auth_details.username, auth_details.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # 生成token有效时间
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # 生成token
        token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        data = {
            "token": token
        }
        return Resp(data=data, message="登录成功")

@router.post('/register', summary="用户注册", response_model=Resp)
async def register(_user: UserRegister):
    """
    用户注册
    Args:
        _user: 用户注册信息
    Returns: 注册结果
    """
    _user = _user.dict()
    async with db_connect.async_session() as session:
        user = User(**_user)
        user.password = get_password_hash(user.password)
        set_default_data(user, '')
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return Resp(message="注册成功")

@router.post('/docsLogin', include_in_schema=False, summary="文档登录")
async def docsLogin(auth_details: OAuth2PasswordRequestForm = Depends()):
    """
    文档登录
    Args:
        auth_details: 用户登录信息
    Returns: 登录结果
    """
    async with db_connect.async_session() as session:
        # 判断用户是否存在
        user = await authenticate_user(session, auth_details.username, auth_details.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # 生成token有效时间
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # 生成token
        token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return Token(access_token=token, token_type="bearer")


@router.post('/info', summary="获取用户详细信息", response_model=Resp)
async def info(current_user_id: User = Depends(get_current_user_id)):
    # 用户名称
    # username = _user.get("userName")
    # username = 'admin'
    async with db_connect.async_session() as session:
        # 查询用户信息
        # result = await session.execute(select(User).where(User.username == username))
        # user = result.scalars().first()
        user = await session.get(User, current_user_id)
        userInfo = UserSer.dump(user)
        # 查询主题信息
        systheme = await get_relationship_data(session, user, Systheme)
        systhemeInfo = SysthemeSer.dump(systheme)
        # 查询菜单信息
        query = select(Menu).join(RoleMenu, RoleMenu.menu_id == Menu.id).join(Role, Role.id == RoleMenu.role_id) \
            .join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user.id)
        query_ = await session.execute(query)
        menuList = query_.scalars().all()
        menuList = await getMenuTree(session, menuList, None)
        menuList = MenuSer.dump(menuList, many=True)
        # print("menuList2 ==> ", menuList)
        data = {
            "userInfo": userInfo,
            "systhemeInfo": systhemeInfo,
            "menuList": menuList
        }
        return Resp(data=data, message="获取用户详细成功")


@router.post('/addOne', summary="新增用户", response_model=Resp)
async def addOne(_user: GetUser, current_user_id: User = Depends(get_current_user_id)):
    """
    新增用户
    Args:
        _user: 用户信息
    Returns: 新增用户结果
    """
    _user = _user.dict()
    roleIds = _user.pop("roleIds")
    # print("current_user_id ==> ", current_user_id)
    async with db_connect.async_session() as session:
        user = User(**_user)
        user.password = get_password_hash(user.password)
        # 设置默认创建人、更新人、创建时间、更新时间
        set_default_data(user, current_user_id)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        # 删除用户角色关联表
        await session.execute(select(UserRole).where(UserRole.user_id == user.id).delete())
        await session.commit()
        # 添加用户角色关系
        userRoleList = [UserRole(user_id=user.id, role_id=roleId,
                                 create_user=current_user_id, update_user=current_user_id,
                                 create_time=datetime.now, update_time=datetime.now) for roleId in roleIds]
        session.add_all(userRoleList)

        return Resp(message="用户添加成功")


@router.post('/deleteById/{id}', summary="删除用户", response_model=Resp)
async def deleteById(id: str, current_user_id: str = Depends(get_current_user_id)):
    """
    删除用户
    Args:
        id: 用户id
    Returns: 删除结果
    """
    async with db_connect.async_session() as session:
        # 删除用户角色关联表
        await session.execute(select(UserRole).where(UserRole.user_id == id).delete())
        # 删除用户
        await session.execute(select(User).where(User.id == id).delete())

        return Resp(message="用户删除成功")


@router.post('/updateById/{id}', summary="更新用户", response_model=Resp)
async def updateById(id: str, _user: UserForm, current_user_id: str = Depends(get_current_user_id)):
    """
    更新用户
    Args:
        id: 用户id
        _user: 用户信息
    Returns: 更新结果
    """
    _user = _user.dict()
    roleIds = _user.pop("roleIds")
    async with db_connect.async_session() as session:
        user = User(**_user)
        set_default_data(user, current_user_id)
        # 更新用户
        await session.execute(select(User).where(User.id == id).update(_user))
        # 删除用户角色关联表
        await session.execute(select(UserRole).where(UserRole.user_id == id).delete())
        # 添加用户角色关系
        userRoleList = [UserRole(user_id=id, role_id=roleId,
                                 create_user=current_user_id, update_user=current_user_id,
                                 create_time=datetime.now, update_time=datetime.now) for roleId in roleIds]
        session.add_all(userRoleList)

        return Resp(message="用户信息修改成功")


@router.get('/findById/{id}', summary="根据id查询用户", response_model=Resp)
async def findById(id: str, current_user_id: str = Depends(get_current_user_id)):
    """
    根据id查询用户
    Args:
        id: 用户id
    Returns: 用户信息
    """
    async with db_connect.async_session() as session:
        # 查询用户信息
        user = await session.get(User, id)
        userSer = UserListSer.dump(user)
        # 查询用户角色信息
        roleList = await get_relationship_data(session, user, Role, UserRole)
        userSer.roleIds = [each.id for each in roleList]
        userSer.roleList = RoleSer.dump(roleList, many=True)
        userSer.systhemeInfo = SysthemeSer.dump(await get_relationship_data(session, user, Systheme))

        return Resp(data=userSer, message="获取用户信息成功")


@router.get('/findList', summary="查询用户列表", response_model=Resp)
async def findList(params: GetPageParams = Depends(), current_user_id: str = Depends(get_current_user_id)):
    """
    查询用户列表
    Returns: 用户列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, User).get_page(session)
        userList = page_data['list']
        userSerList = []
        total = page_data['total']
        relations = params.relations.split(',') if params.relations else []
        for user in userList:
            userSer = UserListSer.dump(user)
            if 'role' in relations or '*' in relations:
                roleList = await get_relationship_data(session, user, Role, UserRole)
                userSer.roleIds = [role.id for role in roleList]
                userSer.roleList = RoleSer.dump(roleList, many=True)
            if 'systheme' in relations or '*' in relations:
                userSer.systhemeInfo = SysthemeSer.dump(await get_relationship_data(session, user, Systheme))
            userSerList.append(userSer)

        data = {
            "userList": userSerList,
            "total": total
        }
        return Resp(data=data, message="获取用户列表成功")


@router.get('/findAll', summary="查询所有用户", response_model=Resp)
async def findAll(params: GetParams = Depends(), current_user_id: str = Depends(get_current_user_id)):
    """
    查询所有用户
    Returns: 用户列表
    """
    async with db_connect.async_session() as session:
        page_data = await Pagination(params, User, all=True).get_page(session)
        userList = page_data['list']
        userSerList = []
        relations = params.relations.split(',') if params.relations else []
        for user in userList:
            userSer = UserListSer.dump(user)
            if 'role' in relations or '*' in relations:
                roleList = await get_relationship_data(session, user, Role, UserRole)
                userSer.roleIds = [role.id for role in roleList]
                userSer.roleList = RoleSer.dump(roleList, many=True)
            if 'systheme' in relations or '*' in relations:
                userSer.systhemeInfo = SysthemeSer.dump(await get_relationship_data(session, user, Systheme))
            userSerList.append(userSer)

        data = {
            "userList": userSerList
        }
        return Resp(data=data, message="查询所有用户成功")


async def getMenuTree(session: AsyncSession, menuList, parentId):
    """
    获取菜单树
    Args:
        session: 数据库连接
        menuList: 菜单列表
        parentId: 父级id
    Returns: 菜单树, 菜单树序列化
    """
    tree = [menu for menu in menuList if menu.superior_id == parentId]
    for menu in tree:
        # 递归获取子级菜单，序列化后的子级菜单
        menu.children = await getMenuTree(session, menuList, menu.id)
        # 获取菜单下的按钮
        menu.atomList = await get_relationship_data(session, menu, Atom, MenuAtom)
    # 返回菜单树和序列化后的菜单树
    return tree
