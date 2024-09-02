
from fastapi import Request

from app.auth.jwt import JWTCookies, JWT
from app.user.dao import DaoUser


async def get_curr_user(request: Request):
    access = JWTCookies.get_cookie_jwt(request, 'access')
    if access is None:
        raise ValueError()

    payload = JWT.decode_token(access)
    JWT.check_expire(payload)
    sub = payload['sub']
    if not sub:
        raise ValueError()

    user = await DaoUser.get_user_by_id(int(sub))
    if not user:
        raise ValueError()
    return user

