from typing import Union
from datetime import date

from sqlalchemy import select

from db.session import BaseDAL
from src.user.models import UserORM


class UserDAL(BaseDAL):
    """Data Access Layer for operating user info"""

    async def create_user(
        self,
        email: str,
        hash_password: str,
        first_name: str,
        last_name: str,
        middle_name: str,
        birth_date: date,
    ) -> UserORM:
        new_user = UserORM(
            email=email,
            hash_password=hash_password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            birth_date=birth_date,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_user_by_email(self, email: str) -> Union[UserORM, None]:
        query = select(UserORM).where(UserORM.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_id(self, uuid) -> Union[UserORM, None]:
        query = select(UserORM).where(UserORM.id == uuid)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
