# coding:utf-8
"""
Name : global_request.py
Author :lvyunze
Time : 2024/1/8 13:33
Desc : 
"""
from json import JSONDecodeError

import simplejson as json
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.types import Message


class GlobalRequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response: StreamingResponse = await call_next(request)
        return response

    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {"type": "http.request", "body": body}

        request._receive = receive

    async def get_body(self, request: Request) -> dict:
        try:
            body = await request.json()
        except JSONDecodeError:
            body = {}
        # 每进入一个中间件，会重新创建一个request对象，但是request._receive只能读取一次
        # 读取body()之后需要重新添加回request
        await self.set_body(request, json.dumps(body).encode())
        return body

    async def set_response_body(self, obj):
        yield obj

    async def get_response_body(self, response):
        body = b""
        async for i in response.body_iterator:
            body += i
        # 同样async_generate只能读取一次，读取之后重新添加回response
        response.body_iterator = self.set_response_body(body)
        return body
