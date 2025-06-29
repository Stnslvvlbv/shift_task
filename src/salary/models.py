from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base, intPk


class ReviewStatusType(Enum):
    PENDING = "Назначен"
    CONSIDER = "Рассматривается"
    APPROVED = "Одобрено"
    PARTIALLY_APPROVED = "Одобрено частично"
    REJECTED = "Отклонено"


class DiscussionOfSalaryIncreaseORM(Base):
    __tablename__ = "salary_increase"

    id: Mapped[intPk]
    user_position_id: Mapped[int] = mapped_column(
        ForeignKey("user_position.id", ondelete="CASCADE"), nullable=False
    )
    requested_salary: Mapped[float] = mapped_column(Numeric(10, 2))
    approved_salary: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    request_datetime: Mapped[datetime] = mapped_column(DateTime())
    status: Mapped[ReviewStatusType] = mapped_column(
        SQLAlchemyEnum(ReviewStatusType, name="review_status_type")
    )
    reasons_increase: Mapped[str] = mapped_column(Text, nullable=False)
    motivation_decision: Mapped[str] = mapped_column(Text, nullable=True)
