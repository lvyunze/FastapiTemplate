from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from starlette import status

from apps.ext.sqlalchemy import db_connect

SECRET_KEY = "b5dc7f4cae55b7d12ac40df5dc0a7409e503fe519f4f08a4d7ad64e1b989f2ea"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/docsLogin")


class TokenData(BaseModel):
    username: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: Union[str, None] = None
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


def verify_password(plain_password, hashed_password):
    """
    验证密码
    :param plain_password: 明文密码
    :param hashed_password: hash密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    加密密码
    :param password: 明文密码
    :return:
    """
    return pwd_context.hash(password)


async def get_user(session, username: str):
    """
    通过用户名称获取用户
    :param db:
    :param username:
    :return:
    """
    # if username in db:
    #     user_dict = db[username]
    #     return UserInDB(**user_dict)
    from apps.ext.sqlalchemy.models import User
    # 查询用户信息
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    return user


async def authenticate_user(session, username: str, password: str):
    """
    验证用户
    :param fake_db:
    :param username:
    :param password:
    :return:
    """
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    生成token
    :param data: 字典数据
    :param expires_delta: 有效时间
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    token获取用户
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload ==> ", payload)
        username: str = payload.get("sub")
        print("username ==> ", username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception:
        raise credentials_exception
    async with db_connect.async_session() as session:
        user = await get_user(session, username=token_data.username)
        if user is None:
            raise credentials_exception
        user = session.merge(user)
        return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    获取当前用户
    :param current_user:
    :return:
    """
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_user_id(current_user: User = Depends(get_current_user)):
    current_user = await current_user
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return str(current_user.id)


if __name__ == '__main__':
    print(get_password_hash("123456"))
