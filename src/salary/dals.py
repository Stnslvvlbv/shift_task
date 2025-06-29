from sqlalchemy import and_, func, select

from db.session import BaseDAL
from src.position.models import UserPositionORM
from src.salary.models import DiscussionOfSalaryIncreaseORM
from src.user.models import UserORM


class SalaryDAL(BaseDAL):
    """Data Access Layer for operating salary info"""

    async def get_future_discussion_of_salary(self, user_uuid: str):

        query = (
            select(DiscussionOfSalaryIncreaseORM)
            .join(
                UserPositionORM,
                UserPositionORM.id == DiscussionOfSalaryIncreaseORM.user_position_id,
            )
            .join(UserORM, UserORM.id == UserPositionORM.user_uuid)
            .where(
                and_(
                    DiscussionOfSalaryIncreaseORM.request_datetime > func.now(),
                    UserPositionORM.user_uuid == user_uuid,
                    UserPositionORM.removed_at.is_(None),
                    UserORM.is_active.is_(True),
                )
            )
        )
        res = await self.db_session.execute(query)
        discussions = res.unique().scalars().all()

        return discussions
