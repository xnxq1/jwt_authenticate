from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy import select
from app.auth.dao import DaoToken
from app.auth.dependencies import get_curr_user
from app.auth.jwt import JWT, JWTCookies
from app.auth.models import RefreshTokenActive
from app.auth.schemas import SchemasForRegister, SchemasForView, SchemasForLogin, SchemasToken
from app.auth.service import AuthService
from app.db import async_sessionfactory
from app.user.dao import DaoUser
from app.user.models import User
router = APIRouter(prefix='/auth', tags=['Authenticate'])
dao_token = DaoToken()
service = AuthService(dao_user=DaoUser(), dao_token=DaoToken())

@router.post('/register')
async def register(user: SchemasForRegister) -> SchemasForView:
    user = await service.register_user(email=user.email, password=user.password, username=user.username)
    await dao_token.add_user_and_token(user.id)
    return user

@router.post('/login')
async def login(user: SchemasForLogin, response: Response) -> SchemasToken:
    tokens = await service.login_user(email=user.email, password=user.password)
    JWTCookies.set_cookie_jwt(response, 'refresh', tokens['refresh'])
    JWTCookies.set_cookie_jwt(response, 'access', tokens['access'])

    return tokens

@router.get('/logout')
async def logout(request: Request, response: Response):
    service.logout_user(request.cookies.get('access'), request.cookies.get('refresh'))
    JWTCookies.delete_cookie_jwt('access', response)
    JWTCookies.delete_cookie_jwt('refresh', response)

@router.get('/refresh')
async def refresh(request: Request, response: Response):
    access_token = await service.refresh_user(request.cookies.get('refresh'))
    JWTCookies.set_cookie_jwt(response, 'access', access_token)


@router.get('/temp1', dependencies=[Depends(get_curr_user)])
async def temp1():
    async with async_sessionfactory() as session:
        query = select(RefreshTokenActive)
        result = await session.execute(query)
        return result.scalars().all()

@router.get('/temp2')
async def temp2():
    async with async_sessionfactory() as session:
        query = select(User)
        result = await session.execute(query)
        return result.scalars().all()