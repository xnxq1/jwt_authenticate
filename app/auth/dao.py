from sqlalchemy import insert

from app.auth.models import RefreshTokenActive
from app.db import async_sessionfactory


class DaoToken:
    __model = RefreshTokenActive


    @classmethod
    async def register_user_to_table(cls, user_id):
        async with async_sessionfactory() as session:
            stmt = insert(cls.__model).values(user_id=user_id)
            await session.execute(stmt)
            await session.commit()
