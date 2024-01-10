import os
import sys

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv("./.env")  # noqa

from apps.app import Client
# 定义FastAPIapp实例的对象
from apps.config.docs import docs

app = FastAPI(
    title=docs.TITLE,
    description=docs.DESC,
    version="V1.0.0",
    # debug 是否再返回结果里面显示错误异常信息
    debug=False,
    docs_url=None,
    redoc_url=None,
    openapi_tags=docs.TAGS_METADATA,
    servers=docs.SERVERS
)

# 初始化app
Client(app)
try:
    port = int(sys.argv[1])
except IndexError:
    port = 9080
debug = os.getenv("ENV_NAME") != "PROD"

if __name__ == "__main__":
    # 启动服务
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        workers=int(os.getenv("uvicorn_workers", 2)),
        use_colors=False,  # 使用颜色会导致log中出现无意义颜色字符串，如[30m，影响log排查
        timeout_keep_alive=int(os.getenv("KEEPALIVE_TIMEOUT", 65))  # 有几率出现连接异常502，server断开连接，但是nginx未断开
    )
