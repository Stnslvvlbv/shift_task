from datetime import date

from sqlalchemy import Text, ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base, str_128, intPk, created_at, updated_at


class PositionORM(Base):
    __tablename__ = "position"

    id: Mapped[intPk]
    name: Mapped[str_128] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    min_salary: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    max_salary: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)


class UserPositionORM(Base):
    __tablename__ = "user_position"

    id: Mapped[intPk]
    user_uuid: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("position.id", ondelete="CASCADE"), nullable=True)
    assigned_salary: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    assigned_at: Mapped[date] = mapped_column(Date, nullable=False)
    removed_at: Mapped[date] = mapped_column(Date, nullable=True)
