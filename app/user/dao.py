
from sqlalchemy import insert, select

from app.user.models import User
from app.db import async_sessionfactory

class DaoUser:
    __model = User

    @classmethod
    async def add_user(cls, **data) -> __model:
        async with async_sessionfactory() as session:
            stmt = insert(cls.__model).values(**data).returning(cls.__model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def get_user_by_email(cls, email: str) -> __model | None:
        async with async_sessionfactory() as session:
            query = select(cls.__model).where(cls.__model.email == email)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

