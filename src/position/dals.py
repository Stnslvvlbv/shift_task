from typing import Union

from sqlalchemy import and_, select

from db.session import BaseDAL
from src.position.models import UserPositionORM
from src.user.models import UserORM


class PositionDAL(BaseDAL):
    """Data Access Layer for operating position info"""

    async def get_current_position(
        self, user_uuid: str
    ) -> Union[UserPositionORM | None]:
        query = (
            select(UserPositionORM)
            .join(UserORM, UserORM.id == UserPositionORM.user_uuid)
            .where(
                and_(
                    UserPositionORM.user_uuid == user_uuid,
                    UserPositionORM.removed_at.is_(None),
                    UserORM.is_active.is_(True),
                )
            )
        )
        res = await self.db_session.execute(query)
        position_row = res.fetchone()
        if position_row is not None:
            return position_row[0]
