# coding:utf-8
"""
Name : json_response.py
Author :lvyunze
Time : 2022/5/16 14:07
Desc : 
"""
from fastapi.responses import JSONResponse, Response
from typing import Union


def resp(data: Union[list, dict, str]) -> Response:
    return JSONResponse(
        {
            "data": data,
            "detail": "ok",
            'error_code': 0,
            "status": "success",
        }
    )


def resp_error(detail: Union[str], status_info: Union[str, int], error_code: int = 1, data: dict = None,
               headers: dict = None) -> Response:
    res = {
        "detail": detail,
        'error_code': error_code,
        "status": status_info
    }
    if data is not None:
        res["data"] = data
    return JSONResponse(res, headers=headers)


def header_msg_resp(message: str = "Records Not Found", data: dict = "") -> Response:
    """
    下载请求无法处理json返回中的数据，通过header来传递信息
    Args:
        message: 需要返回的信息
        data: 预留数据
    """
    return JSONResponse(
        {
            "data": data,
            "detail": "ok",
            "error_code": 0,
            "status": "success",
        },
        headers={"Content-Disposition": message},
    )  # 前端处理数据流时，只能处理header
