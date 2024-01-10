# coding:utf-8
"""
Name : __init__.py.py
Author : blu
Time : 2022/5/16 16:57
Desc : 不应该在这个文件中引用Model类
"""
import contextlib
import logging
import os
from asyncio import current_task
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm import sessionmaker, scoped_session
from apps.config import (
     db_host,
     db_port,
     db_user,
     db_password,
     db_name
)
# 除了配置的导入，这个模块不应该依赖任何其他底层组件，底层组件之间尽量不相互依赖
logger = logging.getLogger(__name__)

print(f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

def get_engine_url(is_async=True) -> str:
    """
    生成数据库连接url,<db_type+driver://user:passwd@host:port/db>
    :param bool is_async: 是否使用异步连接
    :param str db: 数据库
    :return:
    """
    if is_async:
        driver = "aiomysql"
    else:
        driver = "mysqlconnector"
    print(f"mysql+{driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    # 暂时不指定charset，新老系统mysql数据库版本不同，指定编码集会造成异常
    return f"mysql+{driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


class DBManager:

    def __init__(self, engine_options=None, session_options=None, is_async=False):
        """
        :param db: 数据库名
        :param engine_options:
            echo: 是否打印sql语句
            pool_size: 连接池大小
            max_overflow: 并发时允许超过pool_size的连接数量
            pool_timeout: 从连接池中获取连接的等待时间
            pool_recycle: 连接回收时间
        :param session_options:
            autoflush default True,
            autocommit default False,
            expire_on_commit default True: 避免获取属性时重复查询
        :param bool is_async:
        """
        if not engine_options:
            engine_options = {}
        echo_default = os.getenv("ENV_NAME") != "PROD"
        self._engine_options = {"echo": engine_options.pop("echo", echo_default),
                                "pool_size": engine_options.pop("pool_size", 20),
                                "max_overflow": engine_options.pop("max_overflow", 10),
                                "pool_timeout": engine_options.pop("pool_timeout", 100),
                                "pool_recycle": engine_options.pop("pool_recycle", 60 * 60 * 2)}
        self.is_async = is_async
        self.url = get_engine_url(is_async=is_async)
        print("----------------")
        print(self.url)
        self._engine_options.update(engine_options)
        self._session_options = session_options or {}
        # 同步session属性
        self._session_factory = None
        self._session = None
        self._engine = None
        # 异步session属性
        self._async_engine = None
        self._async_factory = None
        self._async_scoped = None

    @property
    def engine(self):
        return self.create_engine()

    @property
    def session_factory(self):
        return self.create_session()

    @property
    def safe_session(self):
        if self.is_async:
            return self.async_safe_session()
        else:
            return self.get_safe_session()

    def create_scoped_session(self, factory, **session_options):
        """
        使用create_session的工厂类，生成sqlalchemy.orm.scoping.scoped_session
        :param factory:
        :param session_options:
        :return:
        """
        scopefunc = session_options.pop("scopefunc", None)
        return scoped_session(factory, scopefunc=scopefunc)

    def create_engine(self):
        """
        生成数据库连接engine，方便内外部调用
        :return:
        """
        if self.is_async:
            if self._async_engine is None:
                self._async_engine = create_async_engine(self.url, **self._engine_options)
            return self._async_engine
        else:
            if self._engine is None:
                self._engine = create_engine(self.url, **self._engine_options)
            return self._engine

    def create_session(self, **session_options):
        """
        返回sqlalchemy.orm.session.sessionmaker生成的工厂类
        :param session_options:
        :return:
        """
        if self.is_async is False:
            self._session_factory = sessionmaker(self.engine, **session_options)
            return self._session_factory
        else:
            self._async_factory = sessionmaker(class_=AsyncSession, bind=self.engine, **session_options)
            return self._async_factory

    def __call__(self, *args, **kwargs):
        """
        生成一个线程安全的sessin会话
        :param args:
        :param kwargs:
        :return:
        """
        if not self._session:
            self._session = self.get_safe_session()
        return self._session()

    def get_safe_session(self):
        """
        线程安全的session，如果单独用这个函数，需要手动remove，例如
        >>> session = apmos_db.get_safe_session()
        >>> res = session.execute("SELECT 1")
        >>> print(res.fetchall())
        [(1,)]
        >>> session.remove()

        :return:
        """
        if not self._session:
            self._session = self.create_scoped_session(self.session_factory, **self._session_options)
        return self._session

    def get_single_session(self):
        """
        单个session连接，线程不安全

        >>> session = apmos_db.get_single_session()
        >>> with session as s:
        >>>     s.execute("select 1")

        :return:
        """
        engine = create_engine(self.url, **self._engine_options)
        factory = sessionmaker(bind=engine)
        conn = engine.connect()
        session = factory(bind=conn, expire_on_commit=False)
        return session

    @contextlib.contextmanager
    def session(self):
        """
        线程安全的session上下文管理

        >>> with apmos_db.session() as session:
        >>>     res = session.execute("SELECT 1")
        >>>     print(res.fetchall())
        [(1,)]

        :return:
        """
        _session = self()
        try:
            yield _session
            _session.commit()
        except Exception as e:
            _session.rollback()
            raise e
        finally:
            self._session.remove()

    async def async_safe_session(self):
        """
        生成一个异步安全的session回话
        :return:
        """
        if not self._async_scoped:
            self._async_scoped = async_scoped_session(self.session_factory, scopefunc=current_task)
        return self._async_scoped

    @contextlib.asynccontextmanager
    async def async_session(self):
        """
        异步session上下文管理封装
        :return:

        >>> async with async_apmos_db.async_session() as session:
        >>>     res = await session.execute("SELECT 1")
        >>>     print(res.scalar())
        1

        """
        scoped = await self.async_safe_session()
        try:
            _session = scoped()
            yield _session
            await self._async_scoped.commit()
        except Exception as e:
            await self._async_scoped.rollback()
            raise e
        finally:
            # 显式的调用engine.dispose，否则会脱离上下文，对象被回收
            # sqlalchemy无法处理异步中的__del__和弱引用，会触发异常
            # RuntimeError: Event loop is closed
            await self._async_engine.dispose()
            await self._async_scoped.remove()


db_connect = DBManager(is_async=True)
