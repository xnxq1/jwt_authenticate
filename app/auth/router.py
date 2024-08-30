from fastapi import APIRouter

from app.auth.dao import DaoToken
from app.auth.schemas import SchemasForRegister, SchemasForView
from app.auth.service import AuthService
from app.user.dao import DaoUser

router = APIRouter(prefix='/auth', tags=['Authenticate'])
dao_user = DaoUser()
dao_token = DaoToken()
service = AuthService(dao_user=dao_user)

@router.post('/register')
async def register(user: SchemasForRegister) -> SchemasForView:
    user = await service.register_user(email=user.email, password=user.password, username=user.username)
    await dao_token.register_user_to_table(user.id)
    return user

@router.post('/login')
async def login():
    pass

@router.post('/logout')
async def logout():
    pass