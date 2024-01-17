from typing import Any

from pydantic import BaseModel


class Resp(BaseModel):
    """
    响应模型
    """
    code: int
    message: str
    data: Any

    def __init__(self, data: Any = None, code: int = 200, message: str = "success"):
        super().__init__(code=code, message=message, data=data)