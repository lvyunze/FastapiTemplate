# coding:utf-8
"""
Name : exception.py
Author : lvyunze
Time : 2022/12/5 9:16
Desc : 
"""
from fastapi import Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, detail):
        self.detail = detail


async def unicorn_exception_handle(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=200,
        content={
            "error_code": 1,
            "detail": exc.detail,
            "status": "error"
        }
    )
