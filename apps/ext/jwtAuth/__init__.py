"""
Author :lvyunze
Desc :
"""
from datetime import datetime, timedelta
import os
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from apps.response.exception import UnicornException


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if os.getenv("ENV_NAME") == "PROD":
        secret = os.getenv('secret')
    else:
        secret = '5VW}yZu@ao-X?ejIr1s{d&S^PTestc'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        exp = datetime.now() + timedelta(days=7)
        iat = datetime.now()
        payload = {
            'exp': int(exp.timestamp()),
            'iat': int(iat.timestamp()),
            'sub': user_id
        }
        try:
            return {
                'token': jwt.encode(
                    payload,
                    self.secret,
                    algorithm='HS256'
                ),
                'iat': int(iat.timestamp()),
                'exp': int(exp.timestamp()),
            }
        except TypeError:
            raise UnicornException("Please configure the server secret key！")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=402, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


auth_handler = AuthHandler()
