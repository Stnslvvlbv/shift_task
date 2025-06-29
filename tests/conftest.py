import asyncio
import os
import subprocess
from typing import Any, Generator
from alembic.config import Config
from alembic import command

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from config import access_settings_db, MODE
from db.database import async_engine, sync_engine
from db.session import get_db
from main import app
from src.user.models import *  # noqa
from src.position.models import *  # noqa
from src.salary.models import *  # noqa
from tests.dataset.user_data import users_list
from tests.db_setter.position_creater import insert_position, insert_user_position
from tests.db_setter.salary_creater import insert_salary_increase
from tests.db_setter.user_creater import create_test_user_sync


class DataControlInsert:
    _instance = None  # Хранение единственного экземпляра класса

    def __new__(cls):
        """
        Создает единственный экземпляр класса при первом вызове.
        При последующих вызовах возвращает уже созданный экземпляр.
        """
        if cls._instance is None:
            cls._instance = super(DataControlInsert, cls).__new__(cls)
            cls._instance.position_added = False
            cls._instance.user_positions_added = False
            cls._instance.salary_increase_added = False
        return cls._instance


@pytest.fixture(scope="function")
def data_control() -> DataControlInsert:
    """
    Фикстура для управления состоянием вставки данных.
    Возвращает единственный экземпляр класса DataControlInsert.
    """
    return DataControlInsert()


@pytest.fixture(scope="function")
def sync_connection():
    """Фикстура для синхронного подключения."""
    with sync_engine.connect() as conn:
        yield conn


@pytest.fixture(scope="function")
async def async_connection():
    """Фикстура для асинхронного подключения."""
    async with async_engine.connect() as conn:
        yield conn


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    assert MODE == "TEST"
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    yield
    # Base.metadata.drop_all(sync_engine)


async def _get_test_db():
    """
    Генератор для создания асинхронной сессии тестовой базы данных.
    """
    test_engine = create_async_engine(
        access_settings_db.DATABASE_URL_ASYNCPG, future=True, echo=True
    )
    test_async_session = async_sessionmaker(
        bind=test_engine, expire_on_commit=False, class_=AsyncSession
    )
    yield test_async_session()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def session_test():
    engine = create_engine(
        access_settings_db.DATABASE_URL_PSYCOPG, future=True, echo=True
    )
    session = sessionmaker(engine, expire_on_commit=False, class_=Session)
    yield session


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
async def set_data_to_user_table(session_test):
    """
    Фикстура для заполнения тестовой базы данных пользователями.
    Проверяет наличие пользователей по списку users_list.
    Создает только тех пользователей, которых нет в базе данных.
    """
    session: Session = session_test()

    if True:
        # Собираем email-адреса из users_list
        expected_emails = {user["email"] for user in users_list}

        # Ищем существующих пользователей в базе данных
        result = session.execute(select(UserORM.email))  # noqa
        existing_emails = {row[0] for row in result.fetchall()}

        # Находим пользователей, которых нужно создать
        missing_emails = expected_emails - existing_emails
        missing_users = [user for user in users_list if user["email"] in missing_emails]

        for user in missing_users:
            # Создаем недостающего пользователя в базе данных
            created_user = create_test_user_sync(session, user)
            user["id"] = created_user.id  # Добавляем ID в users_list
        session.commit()
        session.close()

    return users_list


@pytest.fixture(scope="function")
def get_auth_cookies(client, set_data_to_user_table):
    """
    Фикстура для получения cookies авторизации пользователей с различными конфигурациями.
    """

    async def _get_auth_cookies_callback(user: dict):
        form_data = {
            "username": user["email"],
            "password": user["password"],
        }
        resp_login = client.post(
            "/user/login/",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert resp_login.status_code == 200, f"Login failed for user {user['email']}"

        cookies = {}
        for cookie in resp_login.cookies:
            cookies[cookie] = resp_login.cookies[cookie]

        return cookies

    return _get_auth_cookies_callback


@pytest.fixture(scope="function")
def create_authenticated_client(get_auth_cookies) -> Generator[TestClient, Any, None]:
    """
    Универсальная фикстура для создания тестового клиента с авторизацией.
    Принимает индекс пользователя из users_list.
    """

    async def _create_client(user_index: int):
        try:
            # Переопределяем зависимость get_db для использования тестовой базы данных
            app.dependency_overrides[get_db] = _get_test_db

            # Получаем cookies для указанного пользователя
            cookies = await get_auth_cookies(users_list[user_index])

            # Создаем тестовый клиент с cookies для авторизации
            with TestClient(app, cookies=cookies) as client:
                yield client

        finally:
            # Очищаем переопределения зависимостей после завершения теста
            app.dependency_overrides.clear()

    return _create_client


@pytest.fixture(scope="function")
async def client_for_active_user(
    create_authenticated_client,
) -> Generator[TestClient, Any, None]:
    """
    Фикстура для создания тестового клиента с авторизацией обычного пользователя.
    """
    async for client in create_authenticated_client(0):  # Индекс активного пользователя
        yield client


@pytest.fixture(scope="function")
async def client_for_non_active_user(
    create_authenticated_client,
) -> Generator[TestClient, Any, None]:
    """
    Фикстура для создания тестового клиента с авторизацией обычного пользователя.
    """
    async for client in create_authenticated_client(1):  # Индекс не активного пользователя
        yield client


# Заполнение тестовой базы данных
@pytest.fixture(scope="function")
def inserted_position(session_test, data_control):
    return insert_position(session_test, data_control)


@pytest.fixture(scope="function")
def inserted_user_positions(inserted_position, session_test, data_control, client_for_active_user):
    request = client_for_active_user.get("/user/")
    user_data = request.json()
    user_positions = insert_user_position(user_uuid=user_data["id"], session_test=session_test, data_control=data_control)
    return user_positions


@pytest.fixture(scope="function")
def inserted_salary_increase(inserted_user_positions, session_test, data_control):
    return insert_salary_increase(session_test, data_control)