from sqlalchemy.ext.asyncio import AsyncSession

from src.errors.http_servise_exception import ServiceError
from src.position.dals import PositionDAL
from src.position.shemas import UserPositionSchema


async def _get_current_position_by_user_uuid(
    user_uuid: str, session: AsyncSession
) -> UserPositionSchema:
    async with session.begin():
        dal = PositionDAL(session)
        position = await dal.get_current_position(
            user_uuid=user_uuid,
        )

        if position is None:
            raise ServiceError.not_found()

        return UserPositionSchema.from_orm(position)
