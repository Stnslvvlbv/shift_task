from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import UserORM
from src.security.hasher import Hasher
from src.user.dals import UserDAL
from src.user.schemas import UserRegistrateSchema, UserShowSchema
from src.errors.http_value_exception import LoginExceptions
from src.errors.type_error_ import ServiceAuthException


async def _check_uniqueness_email(email: str, session) -> bool:
    async with session.begin():
        user_dal = UserDAL(session)
        query_user = await user_dal.get_user_by_email(email)
        return False if query_user else True


async def _create_new_user(body: UserRegistrateSchema, session) -> UserShowSchema:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            email=body.email,
            hash_password=Hasher.get_password_hash(body.password),
            first_name=body.first_name,
            last_name=body.last_name,
            middle_name=body.middle_name,
            birth_date=body.birth_date,
        )
        return UserShowSchema.from_orm(user)


async def _get_user_by_uuid(uuid: str, session: AsyncSession) -> Union[UserShowSchema, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            uuid=uuid,
        )

        return UserShowSchema.from_orm(user)


async def _get_user_orm_by_email_for_auth(
    email: str, session: AsyncSession
) -> Union[UserORM, None]:
    async with session as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(
                email=email,
            )


async def _authenticate_user(email: str, password: str, session: AsyncSession) -> Union[UserShowSchema, None]:
    user = await _get_user_orm_by_email_for_auth(email=email, session=session)
    if user is None:
        raise LoginExceptions(ServiceAuthException.UNKNOWING_EMAIL).to_exception("email", "email not registered", email)
    if not Hasher.verify_password(password, user.hash_password):
        raise LoginExceptions(ServiceAuthException.PASSWORD_INVALID).to_exception("password", "the password does not work", "*" * len(password))

    return UserShowSchema.from_orm(user)

