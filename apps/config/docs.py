# coding:utf-8
"""
Name : docs.py
Author : lvyunze
Time : 2024/01/08 11:18
Desc : 
"""
import os
from functools import lru_cache
from pydantic import BaseSettings
import pprint

pp = pprint.PrettyPrinter(indent=4)


class DocsSettings(BaseSettings):
    """配置类"""
    API_V1_STR: str = ""
    # 文档接口描述相关的配置
    DOCS_URL = API_V1_STR + '/docs'
    REDOC_URL = API_V1_STR + '/redocs'
    # OPENAPI_URL配置我们的openapi，json的地址
    OPENAPI_URL = API_V1_STR + '/openapi_url'
    # 接口描述
    TITLE = "管理系统后台"
    # 首页描述文档的详细介绍信息
    DESC = """ apmos 2.0"""
    TAGS_METADATA = [
        {
            "name": "后台管理系统",
            "description": "apmos 2.0",
        },
    ]
    # 配置代理相关的参数信息
    SERVERS = [
        {"url": "/", "description": "本地调试环境"},
        {"url": "https://xx.xx.com", "description": "线上测试环境"},
        {"url": "https://xx2.xx2.com", "description": "线上生产环境"},
    ]
    # 项目根目录
    ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



@lru_cache()
def get_settings():
    return DocsSettings()


# 配置实例的对象的创建
docs = get_settings()