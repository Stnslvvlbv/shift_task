from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.salary.dals import SalaryDAL
from src.salary.schemas import SalaryIncreaseSchema
from src.errors.http_servise_exception import ServiceError


async def _get_future_discussion_of_salary_by_user_uuid(user_uuid: str, session: AsyncSession):
    async with session.begin():
        dal = SalaryDAL(session)
        discussions = await dal.get_future_discussion_of_salary(
            user_uuid=user_uuid,
        )

        return [SalaryIncreaseSchema.from_orm(discussion) for discussion in discussions]
