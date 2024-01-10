# coding:utf-8
"""
Name : validate.py
Author : blu
Time : 2022/6/28 17:01
Desc : 
"""
import datetime
import re

email_regex = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"


def validate_email(email):
    if re.match(email_regex, email) is not None:
        return True
    else:
        return False


def datetime2timestamp(cls, v):
    """
    用于BaseModel的验证方法，将datetime对象转为秒为单位的时间戳
    :param cls:
    :param v:
    :return:
    """
    if isinstance(v, datetime.datetime):
        return v.timestamp()
    return v


def timestamp2datetime(cls, v):
    """
    schema的验证方法，将时间戳转为datetime对象
    :param cls:
    :param v:
    :return:
    """
    if v is None:
        return v
    try:
        return datetime.datetime.fromtimestamp(v)
    except Exception:
        raise ValueError(f"Not a legal second based timestamp: {v}")

