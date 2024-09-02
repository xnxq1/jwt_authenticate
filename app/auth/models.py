from sqlalchemy import ForeignKey

from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column


class RefreshTokenActive(Base):
    __tablename__ = 'RefreshTokenActive'
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), primary_key=True)
    token: Mapped[str | None]