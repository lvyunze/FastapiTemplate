from fastapi import APIRouter, Request
from apps.ext.sqlalchemy.base import metadata, engine
from apps.utils.table import generate_tables, export_tables
import json

router = APIRouter()


@router.post("/create_table")
async def process_data(request: Request):
    # 获取请求体中的JSON数据
    data = await request.body()
    try:
        # 将字节流转换成Python对象
        json_data: dict = json.loads(data)
        table_list: list[dict] = json_data['model']['tableList']
        for table_obj in table_list:
            generate_tables(table_obj)
        metadata.create_all(bind=engine)
        export_tables()
        # 返回结果
        return {"message": "The database table has been created successfully"}
    except Exception as e:
        # 发生错误时返回错误信息
        return {"error": str(e)}
