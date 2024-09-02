from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.config import settings
from fastapi import Response, Request


from passlib.context import CryptContext
CONST_REFRESH_EXPIRE = datetime.utcnow() + timedelta(days=30)
CONST_ACCESS_EXPIRE = datetime.utcnow() + timedelta(minutes=2)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)


class JWT:

    @classmethod
    def _create_token(cls, user_id: int, expire: datetime, type_token: str) -> str:
        data = {'sub': str(user_id), 'exp': expire, 'type': type_token}
        token = jwt.encode(data, key=settings.SECRETKEY, algorithm=settings.ALGORITHM)
        return token

    @classmethod
    def create_refresh_token(cls, user_id: int) -> str:
        return cls._create_token(user_id=user_id, expire=CONST_REFRESH_EXPIRE, type_token='refresh')

    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        return cls._create_token(user_id=user_id, expire=CONST_ACCESS_EXPIRE, type_token='access')

    @classmethod
    def decode_token(cls, token) -> dict:
        payload = jwt.decode(token, settings.SECRETKEY, settings.ALGORITHM)
        return payload

    @classmethod
    def check_expire(cls, payload: dict):
        expire = payload['exp']
        if not expire or int(expire) < datetime.utcnow().timestamp():
            raise ValueError()


class JWTCookies:

    @classmethod
    def set_cookie_jwt(cls, responce: Response, token_type: str, token: str):
        responce.set_cookie(key=token_type, value=token, httponly=True)

    @classmethod
    def get_cookie_jwt(cls, request: Request, token_type: str):
        token = request.cookies.get(token_type)
        return token

    @classmethod
    def delete_cookie_jwt(cls, token_type:str, responce: Response):
        responce.delete_cookie(token_type)




