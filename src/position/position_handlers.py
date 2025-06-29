from typing import Optional

from authx import RequestToken
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from src.position.actions import _get_current_position_by_user_uuid
from src.position.shemas import UserPositionSchema
from src.security.auth import security

position_router: APIRouter = APIRouter()


@position_router.get(
    "/current",
    dependencies=[Depends(security.get_optional_access_from_request)],
    response_model=UserPositionSchema,
    summary="Текущая должность и назначенная зароботная плата",
    description="""
    Должность.
    - Доступно только для активных пользователей.
    - Возвращает текущую должность с описанием и заработной платой.
    """,
)
async def get_current_position(
    db: AsyncSession = Depends(get_db),
    token: Optional[RequestToken] = Depends(security.get_optional_access_from_request),
) -> UserPositionSchema:

    token_payload = security.validate_token(token)
    security.checking_user_rights(token_payload, is_active=True)
    current_position = await _get_current_position_by_user_uuid(
        user_uuid=token_payload.sub, session=db
    )

    return current_position
