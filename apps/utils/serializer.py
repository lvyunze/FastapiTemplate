import re
from decimal import Decimal
from typing import Type, Container, Optional, overload, Annotated

from pydantic import BaseModel, create_model, BaseConfig, Field
from sqlalchemy import inspect
from sqlalchemy.orm import ColumnProperty


def dump(cls, objs, many=False, **kwargs):
    """
    用于序列化数据
    Args:
        cls: SQLAlchemy模型类，用于创建模型实例。
        objs: SQLAlchemy模型对象或对象列表，需要被序列化的数据。
        many: 布尔值，如果为True，表示`objs`是一个对象列表。如果为False，表示`objs`是一个单一对象。
        **kwargs: 额外的参数，将被传递给`dict()`方法，用于控制序列化的行为。
    Returns:
        如果`many`为True，返回一个字典列表。如果`many`为False，返回一个字典
    """
    if not objs:
        return [] if many is True else {}
    if many is True:
        # 如果是批量序列化，遍历`objs`列表，对每个对象进行序列化
        return [cls.from_orm(obj) for obj in objs]
    # 如果是单一对象，直接序列化
    return cls.from_orm(objs)


class OrmConfig(BaseConfig):
    """
    orm模式配置
    """
    orm_mode = True
    allow_population_by_field_name = True


def underscore_to_camelcase(value):
    """
    下划线风格转小驼峰
    Args:
        value: 下划线风格字符串
    Returns: 小驼峰字符串
    """
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), value)


def model2schema(
        db_model: Type,
        *,  # 以下参数必须使用关键字传参
        config: Type = OrmConfig,
        include: Container[str] = None,
        exclude: Container[str] = None,
) -> Type[BaseModel]:
    """
    用sqlalchemy model生成BaseModel子类，默认注册所有字段，可以用include、exclude控制字段
    :param db_model: sqlalchemy model
    :param config: orm模式配置
    :param include: 包含的字段
    :param exclude: 排除的字段
    :return: BaseModel子类
    """
    exclude = exclude or []
    include = include or []
    # 获取model的属性
    mapper = inspect(db_model)
    fields = {}
    for attr in mapper.attrs:
        # 如果是ColumnProperty,说明是数据库模型字段；如果有columns，说明是数据库表字段
        if isinstance(attr, ColumnProperty) and attr.columns:
            # 获取字段名
            name = attr.key
            # 排除不需要的字段
            if (include and name not in include) or (name in exclude):
                continue

            # 获取字段类型
            column = attr.columns[0]
            # 获取字段类型对应的python类型
            python_type: Optional[type] = None

            # 如果字段类型有python_type属性
            if hasattr(column.type, "python_type"):
                python_type = column.type.python_type
                # 如果字段类型有impl属性
                if hasattr(column.type, "impl"):
                    python_type = column.type.impl.python_type
            # 如果python_type为None，抛出异常
            assert python_type, f"Could not infer python_type for {column}"
            # 如果python类型是Decimal，转换成float
            python_type = python_type if not issubclass(python_type, Decimal) else float

            # 如果字段没有默认值，且不可为空，设置默认值为...
            default = None
            if column.default is None and not column.nullable:
                default = ...
            # 设置字段
            # fields[name] = (python_type, default)
            # 设置字段，将字段名转换成小驼峰
            fields[name] = (python_type,Field(default, alias=underscore_to_camelcase(name)))

    # 创建BaseModel子类
    model = create_model(db_model.__name__, __config__=config, **fields)
    # 设置dump方法
    model.dump = classmethod(dump)
    # 返回BaseModel子类
    return model
