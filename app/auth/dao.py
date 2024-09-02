from sqlalchemy import insert, update, select

from app.auth.models import RefreshTokenActive
from app.db import async_sessionfactory


class DaoToken:
    __model = RefreshTokenActive


    @classmethod
    async def add_user_and_token(cls, user_id: int, token: str | None = None):
        async with async_sessionfactory() as session:
            stmt = insert(cls.__model).values(user_id=user_id, token=token)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def update_token(cls, user_id: int, token: str):
        async with async_sessionfactory() as session:
            stmt = update(cls.__model).where(cls.__model.user_id==user_id).values(token=token)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_token_by_user_id(cls, user_id: int):
        async with async_sessionfactory() as session:
            query = select(cls.__model).where(cls.__model.user_id == user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
