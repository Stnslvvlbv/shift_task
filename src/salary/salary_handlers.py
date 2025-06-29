from typing import List, Optional

from authx import RequestToken
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from src.salary.actions import _get_future_discussion_of_salary_by_user_uuid
from src.salary.schemas import SalaryIncreaseSchema
from src.security.auth import security

salary_router: APIRouter = APIRouter()


@salary_router.get(
    "/future_increase",
    dependencies=[Depends(security.get_optional_access_from_request)],
    response_model=List[SalaryIncreaseSchema],
    summary="Назначенные рассмотрения повышения заработной платы.",
    description="""
    Рассмотрения заработной платы.
    - Доступно только для активных пользователей.
    - Возвращает список предстоящих рассмотрений повышения оплаты труда.
    """,
)
async def get_future_discussion_salary(
    db: AsyncSession = Depends(get_db),
    token: Optional[RequestToken] = Depends(security.get_optional_access_from_request),
) -> List[SalaryIncreaseSchema]:

    token_payload = security.validate_token(token)
    security.checking_user_rights(token_payload, is_active=True)
    discussion = await _get_future_discussion_of_salary_by_user_uuid(
        user_uuid=token_payload.sub, session=db
    )

    return discussion
