from fastapi import FastAPI, APIRouter, Depends

from apps.utils.security import get_current_user
from .role import router as role_router
from .user import router as user_router
from .file import router as file_router
from .menu import router as menu_router
from .atom import router as atom_router
from .systheme import router as systheme_router
from .dict import router as dict_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["用户管理"])
router.include_router(role_router, prefix="/role", tags=["角色管理"], dependencies=[Depends(get_current_user)])
router.include_router(menu_router, prefix="/menu", tags=["菜单管理"], dependencies=[Depends(get_current_user)])
router.include_router(atom_router, prefix="/atom", tags=["原子管理"], dependencies=[Depends(get_current_user)])
router.include_router(systheme_router, prefix="/systheme", tags=["主题管理"], dependencies=[Depends(get_current_user)])
router.include_router(dict_router, prefix="/dict", tags=["字典管理"], dependencies=[Depends(get_current_user)])
router.include_router(file_router, prefix="/upload", tags=["文件管理"], dependencies=[Depends(get_current_user)])


# 注册路由
def register_router_v1(app: FastAPI):
    # 路由集合
    app.include_router(router)
