# -*- coding: utf-8 -*-
# @Name    : admin.py
# @Author  : lvyunze
# @Time    : 2024/1/10 21:14
# @Desc
from fastapi import APIRouter
from sqlalchemy import select
from apps.ext.jwtAuth import auth_handler
from apps.modules.user.schemas.user import AuthDetails
# from apps.ext.sqlalchemy.model import User
from fastapi_extend import PageNumberPagination
from apps.ext.sqlalchemy import db_connect
from apps.modules.user.schemas.user import GetUser, UserSer
from apps.response.json_response import resp
from fastapi import Depends

router = APIRouter()


@router.post('/index')
async def login(auth_details: AuthDetails):
    payload = {
        "userName": auth_details.username.lower()
    }
    token = auth_handler.encode_token(payload)
    return resp(data={"Authorization": token})

