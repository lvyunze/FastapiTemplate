# coding: utf-8
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, JSON, String, Text, text
from sqlalchemy.dialects.mysql import CHAR, INTEGER, TINYINT
from sqlalchemy.orm import relationship
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

metadata = Base.metadata


class Atom(Base):
    __tablename__ = 'atom'

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    name = Column(String(255), nullable=False, comment='按钮名称')
    sort = Column(INTEGER(20), comment='排序')
    describe = Column(String(255), comment='按钮描述')
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    update_time = Column(DateTime, nullable=False, comment='更新时间')


class Dict(Base):
    __tablename__ = 'dict'

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    name = Column(String(255), nullable=False, comment='字典名称')
    type = Column(INTEGER(255), nullable=False, comment='字典类型')
    sort = Column(INTEGER(255), comment='排序')
    status = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='状态: 0: 禁用, 1: 开启')
    describe = Column(String(255), comment='描述')
    values = Column(JSON, nullable=False, comment='字典值')
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    update_time = Column(DateTime, nullable=False, comment='更新时间')


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    name = Column(String(255), nullable=False, comment='首页的组件名称')
    path = Column(String(255), nullable=False, comment='菜单路径')
    grade = Column(INTEGER(20), nullable=False, comment='菜单等级')
    superior_id = Column(String(255), comment='父级菜单id,如果没有,则为null')
    menu_type = Column(INTEGER(8), nullable=False, comment='菜单类型: 1: 目录, 2: 菜单')
    sort = Column(INTEGER(20), comment='排序')
    is_out_lint = Column(TINYINT(1), nullable=False, comment='是否外链')
    out_lint = Column(String(255), comment='外链地址')
    meta = Column(JSON, nullable=False, comment='菜单的其他信息(名称 + icon)')
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    update_time = Column(DateTime, nullable=False, comment='更新时间')
    hidden = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='是否隐藏菜单')


class Role(Base):
    __tablename__ = 'role'

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    name = Column(String(255), nullable=False, comment='角色名称')
    parent_id = Column(String(255), comment='角色的父级id')
    sort = Column(INTEGER(20), comment='排序')
    status = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='角色状态: 0: 禁用, 1: 开启')
    code = Column(String(255), nullable=False, comment='角色')
    describe = Column(String(255), comment='角色描述')
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    update_time = Column(DateTime, nullable=False, comment='更新时间')


class Systheme(Base):
    __tablename__ = 'systheme'

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    logo = Column(String(255), server_default=text("''"), comment='系统logo图片地址')
    is_show_logo = Column(TINYINT(1), server_default=text("'0'"), comment='是否展示logo')
    theme_colors = Column(String(255), server_default=text("''"), comment='主题颜色')
    theme_scheme = Column(String(255), server_default=text("''"), comment='主题方法: 菜单颜色 + 顶部颜色 + 背景颜色')
    fixed_header = Column(TINYINT(1), server_default=text("'0'"), comment='固定顶部不滑动')
    btn_size = Column(String(255), nullable=False, server_default=text("''"), comment='按钮大小')
    font_size = Column(String(255), server_default=text("''"), comment='字体大小')
    ipt_size = Column(String(255), nullable=False, server_default=text("''"), comment='输入框类型大小')
    is_show_top_cache_menu = Column(TINYINT(1), server_default=text("'0'"), comment='是否展示顶部缓存的')
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, nullable=False, comment='创建时间')
    update_time = Column(DateTime, nullable=False, comment='更新时间')


class User(Base):
    __tablename__ = 'user'

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    name = Column(String(255), nullable=False, comment='角色名称')
    sort = Column(INTEGER(20), comment='排序')
    status = Column(TINYINT(1), nullable=False, server_default=text("0"), comment='角色状态: 0: 禁用, 1: 开启')
    avatar = Column(String(255), comment='用户名')
    username = Column(String(255), nullable=False, unique=True, comment='登录账号')
    password = Column(String(255), nullable=False, comment='登录密码')
    introduction = Column(String(255), comment='描述')
    systheme_id = Column(String(255), comment='描述')
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False,
                         comment='更新时间')


class MenuAtom(Base):
    __tablename__ = 'menu_atom'
    __table_args__ = (
        Index('menu_atom_menu_id_atom_id_unique', 'atom_id', 'menu_id', unique=True),
    )

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    menu_id = Column(ForeignKey('menu.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    atom_id = Column(ForeignKey('atom.id', ondelete='CASCADE', onupdate='CASCADE'))
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')

    atom = relationship('Atom')
    menu = relationship('Menu')


class RoleAtom(Base):
    __tablename__ = 'role_atom'
    __table_args__ = (
        Index('role_atom_role_id_atom_id_unique', 'atom_id', 'role_id', unique=True),
    )

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    role_id = Column(ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    atom_id = Column(ForeignKey('atom.id', ondelete='CASCADE', onupdate='CASCADE'))
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')

    atom = relationship('Atom')
    role = relationship('Role')


class RoleMenu(Base):
    __tablename__ = 'role_menu'
    __table_args__ = (
        Index('role_menu_menu_id_role_id_unique', 'role_id', 'menu_id', unique=True),
    )

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    menu_id = Column(ForeignKey('menu.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    role_id = Column(ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'))
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')

    menu = relationship('Menu')
    role = relationship('Role')


class UserRole(Base):
    __tablename__ = 'user_role'
    __table_args__ = (
        Index('user_role_role_id_user_id_unique', 'user_id', 'role_id', unique=True),
    )

    id = Column(CHAR(36), primary_key=True, default=text("(UUID())"), comment='主键id')
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    role_id = Column(ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    create_user = Column(CHAR(36), nullable=False, comment='创建人的id')
    update_user = Column(CHAR(36), nullable=False, comment='创建人的id 、每次更新的是自动更新该字段')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')

    role = relationship('Role')
    user = relationship('User')
