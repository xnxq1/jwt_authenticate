from sqlalchemy.orm import Mapped, mapped_column

from app.models import intpk, Base


class User(Base):
    __tablename__ = 'User'
    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)