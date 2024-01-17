import json
from os import getenv, popen
from os.path import dirname, join, abspath
from apps.config.types import type_obj
from typing import Union
from sqlalchemy import Table, Column, text, JSON, ForeignKey
from apps.ext.sqlalchemy.base import metadata, engine


def load_from_local() -> None:
    """
    本地通过template.json文件直接动态加载
    """
    try:
        json_path = abspath(join(dirname(__file__), '../../.template.json'))
        with open(json_path) as fp:
            json_data: dict = json.loads(fp.read())
            print(json_data)
            table_list: list[dict] = json_data['model']['tableList']
            for table_obj in table_list:
                generate_tables(table_obj)
            metadata.create_all(bind=engine)
            export_tables()
    except Exception as e:
        print(e)


def export_tables() -> None:
    """
    将数据库表导出Models
    """
    file_path = abspath(join(dirname(__file__), '../models/models.py'))
    popen(f'sqlacodegen {getenv("DATABASE_URL")} > {file_path}')


def handle_field_default(field_default):
    """
    处理表字段的默认值
    """
    if isinstance(field_default, bool):
        bool_dict = {True: '1', False: '0'}
        return text(bool_dict[field_default])
    if isinstance(field_default, str):
        return text(str(field_default))
    return field_default


def handle_field_type(field: dict):
    """
    处理表字段的存储类型
    """
    if 'hasMany' in field and field.get('hasMany') is True:
        return JSON
    obj_type = field.get('type')
    field_type = type_obj.get(obj_type)
    return field_type


def handle_foreign_key(foreign_obj: dict, curr_column_name: str = '') -> Union[str, tuple]:
    """
    处理外键关联字段关系，针对one to one和many to one的情况
    """
    simple_types: list = ['oneToOne', 'oneToOneWay', 'manyToOne', 'manyToOneWay']
    complex_types: list = ['manyToMany', 'manyToManyWay']
    foreign_type = foreign_obj.get('type')
    junction_table: dict = foreign_obj.get('junctionTable')
    table_name = junction_table.get('tableName')
    junction_key = junction_table.get('junctionKey')
    foreign_key = f'{table_name}.{junction_key}'
    column_name = f'{table_name}_{junction_key}'
    if column_name == curr_column_name and foreign_type in simple_types:
        return foreign_key
    if foreign_type in complex_types:
        return table_name, column_name, foreign_key


def handle_foreign_table(foreigners: list[dict], curr_table_name) -> None:
    """
    处理双表关联关系，生成一张关联关系表，针对many to many的情况
    """
    for foreign_obj in foreigners:
        result = handle_foreign_key(foreign_obj)
        if isinstance(result, tuple):
            junction_table_name = result[0]
            junction_column_name = result[1]
            junction_foreign_key = result[2]
            curr_column_name = f'{curr_table_name}_id'
            curr_foreign_key = f'{curr_table_name}.id'
            table_name = f'{junction_table_name}_{curr_table_name}'
            table = Table(
                table_name,
                metadata,
                Column('id', type_obj.get('id'), primary_key=True, default=text("(UUID())"), comment='主键id')
            )
            column1 = Column(curr_column_name, ForeignKey(curr_foreign_key, ondelete='CASCADE', onupdate='CASCADE'))
            column2 = Column(
                junction_column_name,
                ForeignKey(junction_foreign_key, ondelete='CASCADE', onupdate='CASCADE')
            )
            table.append_column(column1)
            table.append_column(column2)


def handle_column(obj: dict, foreign_key: Union[str, None] = '') -> Column:
    """
    处理具体每个表的字段
    """
    column_name = obj.get('columnName')
    column_comment = obj.get('comment')
    column_type = handle_field_type(obj)
    is_unique: bool = 'unique' in obj and obj.get('unique') is True
    is_nullable: bool = 'required' not in obj
    if foreign_key:
        column = Column(column_name, ForeignKey(foreign_key, ondelete='CASCADE', onupdate='CASCADE'))
    else:
        column = Column(column_name, column_type, comment=column_comment, nullable=is_nullable, unique=is_unique)
        if 'default' in obj:
            default = handle_field_default(obj.get('default'))
            setattr(column, 'server_default', default)
    return column


def generate_tables(table_obj: dict) -> None:
    """
    处理动态生成表
    """
    table_name = table_obj.get('tableName')
    table = Table(
        table_name,
        metadata,
        Column('id', type_obj.get('id'), primary_key=True, default=text("(UUID())"), comment='主键id')
    )
    columns: list[dict] = table_obj.get('columns')
    foreigners: list[dict] = table_obj.get('foreigns')
    for obj in columns:
        for foreign_obj in foreigners:
            foreign_key = handle_foreign_key(foreign_obj, obj.get('columnName'))
            if foreign_key and isinstance(foreign_key, str):
                column = handle_column(obj, foreign_key)
                table.append_column(column)
                break
        else:
            column = handle_column(obj)
            table.append_column(column)
    handle_foreign_table(foreigners, table_name)


if __name__ == '__main__':
    load_from_local()
