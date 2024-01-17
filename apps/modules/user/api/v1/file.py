import os
from fastapi import APIRouter, UploadFile

from apps.config.docs import docs
from apps.utils.response import Resp

router = APIRouter(tags=["文件管理"])


@router.post('/upload', summary="文件上传", response_model=Resp)
async def upload(file: UploadFile):
    # 上传文件目录
    UPLOAD_DIR = os.path.join(docs.ROOT_PATH, 'uploads')
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        for line in file.file:
            f.write(line)

    data = {
        "path": os.path.join('uploads', file.filename)
    }
    return Resp(data=data, message="文件上传成功")