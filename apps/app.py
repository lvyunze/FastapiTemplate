# coding:utf-8
"""
Name : app.py
Author :lvyunze
Time : 2022/5/16 11:16
Desc : 全局app，用于初始化相关配置
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from apps.modules.user.api.v1 import register_router_v1


class Client:

    def __init__(self, app: FastAPI):
        self.app = app
        self.register_global_exception()
        self.register_global_cors()  # 全局配置跨域设置
        self.register_global_middleware()  # 配置中间件
        # self.register_global_include_router()  # 批量导入注册路由
        register_router_v1(app) # 单独注册路由

    def register_global_cors(self):
        """
        處理全局跨域
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["Content-Disposition"]
        )

    def register_global_middleware(self):
        # from apps.middleware.global_permission import GlobalPermissionMiddleware
        # from apps.middleware.global_request import GlobalRequestMiddleware
        pass
        # 中间件执行顺序，后注册的先执行
        # 在栈顶中间件记录request时，call_next会返回一个StreamResponse，导致block在listen_for_disconnect
        # self.app.add_middleware(GlobalRequestMiddleware)
        # self.app.add_middleware(GlobalPermissionMiddleware)

    def register_global_include_router(self):
        """
        导入路由模块
        :return:
        """
        from apps.utils.routes import RouterHelper
        RouterHelper = RouterHelper()
        router_list = RouterHelper.file_router()
        # 将router添加到app当中
        for each in router_list:
            print(router_list)
            self.app.include_router(each['client'], prefix=f'/api/{each["version"]}/{each["module"]}')

    def register_global_exception(self):
        from apps.response.exception import UnicornException, unicorn_exception_handle
        self.app.add_exception_handler(UnicornException, unicorn_exception_handle)

    def mount_static_files(self):
        # 装载静态目录
        from starlette.staticfiles import StaticFiles
        import os
        # 项目根目录
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # 静态文件目录
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        self.app.mount("/static", StaticFiles(directory=STATIC_DIR))
