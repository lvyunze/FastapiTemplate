import os
from fastapi import APIRouter, UploadFile

from apps.config.docs import docs

router = APIRouter(tags=["文件管理"])


@router.post('/upload', summary="文件上传")
async def upload(file: UploadFile):
    # 上传文件目录
    UPLOAD_DIR = os.path.join(docs.ROOT_PATH, 'uploads')
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        for line in file.file:
            f.write(line)
    res = {
        "code": 200,
        "message": "文件上传成功",
        "data": {
            "path": os.path.join('uploads', file.filename)
        }
    }
    return res