from sqlalchemy import DateTime, Float, Integer, JSON, String
from sqlalchemy.dialects.mysql import TINYINT

type_obj = {
    'int': Integer,
    'float': Float,
    'string': String(256),
    'password': String(256),
    'email': String(256),
    'textarea': String(256),
    'boolean': TINYINT(1),
    'richtext': String(256),
    'date': DateTime,
    'imgUrl': String(256),
    'soundUrl': String(256),
    'videoUrl': String(256),
    'radio': String(256),
    'enums': JSON,
    'enum': String(256),
    'id': String(36),
    'checked': JSON,
}
