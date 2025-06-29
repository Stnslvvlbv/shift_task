import uuid
from datetime import date

from sqlalchemy import Column, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base, created_at, str_32, str_256


class UserORM(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    first_name: Mapped[str_32] = mapped_column(nullable=False)
    middle_name: Mapped[str_32] = mapped_column(nullable=True)
    last_name: Mapped[str_32] = mapped_column(nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    hash_password: Mapped[str_256] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(default=True)
