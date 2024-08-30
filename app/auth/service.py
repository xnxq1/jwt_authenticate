from dataclasses import dataclass

from app.user.dao import DaoUser
from app.auth.dependencies import Hasher

@dataclass
class AuthService:
    dao_user: DaoUser

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
