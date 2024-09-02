from dataclasses import dataclass

from app.auth.dao import DaoToken
from app.user.dao import DaoUser
from app.auth.jwt import Hasher, JWT


@dataclass
class AuthService:
    dao_user: DaoUser
    dao_token: DaoToken

    async def register_user(self, **data):
        exist_user = await self.dao_user.get_user_by_email(email=data.get('email'))
        if exist_user:
            raise ValueError()
        data['password'] = Hasher.get_password_hash(data.get('password'))
        try:
            user = await self.dao_user.add_user(**data)
            return user
        except:
            raise Exception()

    async def login_user(self, email: str, password: str):
        exist_user = await self.dao_user.get_user_by_email(email=email)
        exist_user_data = exist_user.__dict__
        if exist_user is None or not Hasher.verify_password(password, exist_user_data['password']):
            raise ValueError()
        refresh_token = JWT.create_refresh_token(exist_user_data['id'])
        await self.dao_token.update_token(exist_user_data['id'], refresh_token)
        access_token = JWT.create_access_token(exist_user_data['id'])
        return {'refresh': refresh_token, 'access': access_token}


    def logout_user(self, access, refresh):
        if access is None and refresh is None:
            raise ValueError()


    async def refresh_user(self, refresh: str):
        if refresh is None:
            raise ValueError()
        try:
            payload = JWT.decode_token(refresh)
            user_id = int(payload['sub'])
        except:
            raise ValueError()

        JWT.check_expire(payload)
        token_in_db = await self.dao_token.get_token_by_user_id(user_id)
        token_in_db = token_in_db.__dict__
        if token_in_db is None or refresh != token_in_db['token']:
            raise ValueError()
        access_token = JWT.create_access_token(user_id)
        return access_token

