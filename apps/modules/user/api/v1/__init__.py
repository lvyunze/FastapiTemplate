from fastapi import FastAPI, APIRouter, Depends

from apps.utils.security import get_current_user
from .user import router as user_router
from .file import router as file_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["用户管理"])
router.include_router(file_router, prefix="/upload", tags=["文件管理"], dependencies=[Depends(get_current_user)])


# 注册路由
def register_router_v1(app: FastAPI):
    # 路由集合
    app.include_router(router)
