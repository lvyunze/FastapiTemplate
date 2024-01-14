# coding: utf-8
from sqlalchemy import (
    BigInteger,
    DECIMAL,
    Date,
    DateTime,
    Index,
    JSON,
    TIMESTAMP,
    Text,
    text,
    Column,
    Integer,
    String
)
from sqlalchemy.dialects.mysql import CHAR, INTEGER, TEXT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


def to_dict(self):
    """
    每个表模型的数据转换为字典
    """
    result = {}
    for key in self.__mapper__.c.keys():
        if isinstance(getattr(self, key), (dict, list)):
            result[key] = getattr(self, key)
        else:
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
    return result


# 在Base当中添加该方法，其他类继承Base类都会继承该方法
Base.to_dict = to_dict


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     username = Column(VARCHAR(16), comment='用户名')
#     password = Column(VARCHAR(16), comment='密码')
#     update_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

