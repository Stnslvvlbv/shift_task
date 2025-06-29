from typing import Annotated, Optional

from authx import RequestToken
from fastapi import APIRouter, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from src.errors.http_value_exception import FieldExceptions
from src.errors.type_error_ import FieldCodeExceptions
from src.security.auth import security
from src.user.actions import _check_uniqueness_email, _create_new_user, _authenticate_user, _get_user_by_uuid
from src.user.schemas import UserRegistrateSchema, UserShowSchema, UserDataFromTokenSchema

user_router: APIRouter = APIRouter()


"""Блок безопасности пользователя"""


@user_router.post(
    "/registrate",
    summary="Регистрация пользователя",
    description="""
    Регистрация нового пользователя.
    - **email**: Уникальный email пользователя.
    - **password**: Пароль пользователя (минимум 8 символов).
    - **first_name**: Имя пользователя.
    - **last_name**: Фамилия пользователя.
    - **birth_date**: Дата рождения в формате YYYY-MM-DD.
    """,
    response_model=UserShowSchema
)
async def registrate(
    body: UserRegistrateSchema, db: AsyncSession = Depends(get_db)
) -> UserShowSchema:
    unique_email = await _check_uniqueness_email(body.email, db)

    if unique_email:
        return await _create_new_user(body, db)

    raise FieldExceptions(FieldCodeExceptions.EMAIL_NOT_UNIQUE).to_exception("email", "A user with this email already exists.", body.email)


@user_router.post(
    "/login",
    summary="Авторизация пользователя",
    description="""
    Авторизация пользователя с использованием email и пароля.
    - Возвращает access и refresh токены в cookies.
    """,
    response_model=UserShowSchema,
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> UserShowSchema:
    user = await _authenticate_user(form_data.username, form_data.password, db)

    user_data = UserDataFromTokenSchema(**user.dict())
    access_token = security.create_access_token(uid=str(user.id), fresh=True, data=user_data.dict())

    refresh_token = security.create_refresh_token(uid=str(user.id))

    security.set_access_cookies(response=response, token=access_token)
    security.set_refresh_cookies(response=response, token=refresh_token)
    return user


@user_router.post(
    "/refresh",
    summary="Обновление access токена с использованием refresh токена",
    description="""
    Обновление access токена с использованием refresh токена.
    - Refresh токен должен быть передан в cookies.
    - Возвращает новый access в cookies файле.
    """,
)
async def refresh_token(
    response: Response,
    token: Optional[RequestToken] = Depends(security.get_optional_refresh_from_request),
    db: AsyncSession = Depends(get_db),
):
    refresh_payload = security.validate_token(token)
    user = await _get_user_by_uuid(refresh_payload.sub, db)

    user_data = UserDataFromTokenSchema(**user.dict())
    access_token = security.create_access_token(
        uid=str(user.id), fresh=False, data=user_data.dict()
    )
    security.set_access_cookies(response=response, token=access_token)
    return {
        "message": "Access token refreshed successfully",
    }


@user_router.get(
    "/",
    dependencies=[Depends(security.get_optional_access_from_request)],
    summary="Получение данных текущего пользователя",
    description="""
    Получение данных авторизованного пользователя.
    - Требуется передача access токена в cookies.
    """,
)
async def get_user_by_access_token(
    db: AsyncSession = Depends(get_db),
    token: Optional[RequestToken] = Depends(security.get_optional_access_from_request),
) -> UserShowSchema:

    token_payload = security.validate_token(token)
    user_uuid = token_payload.sub

    user = await _get_user_by_uuid(user_uuid, db)
    return user


@user_router.post(
    "/logout",
    dependencies=[Depends(security.get_optional_access_from_request)],
    summary="Выход из системы",
    description="""
    Выход из системы.
    - Заносит access и refresh токены в черный список.
    """,
)
def logout(
    access_token: RequestToken = Depends(security.get_optional_access_from_request),
    refresh_token: Optional[RequestToken] = Depends(
        security.get_optional_refresh_from_request
    ),
):
    message = ""
    message += security.check_validity_and_block(access_token, "access") + ". "
    message += security.check_validity_and_block(refresh_token, "refresh") + "."

    return {"detail": message}
