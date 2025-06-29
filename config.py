import logging
import os
from datetime import timedelta

from authx import AuthXConfig
from dotenv import load_dotenv

MAX_LIMIT_PAGINATE = 50

logging.basicConfig(
    filename="fast_api.log",  # Логи будут сохраняться в файл
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()
MODE = os.getenv("MODE")

JWT_TOKEN_CONFIG = AuthXConfig()
JWT_TOKEN_CONFIG.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
JWT_TOKEN_CONFIG.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=20)

JWT_TOKEN_CONFIG.JWT_ALGORITHM = "HS256"
JWT_TOKEN_CONFIG.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_TOKEN_CONFIG.JWT_TOKEN_LOCATION = [
    "cookies",
]
JWT_TOKEN_CONFIG.JWT_CSRF_IN_COOKIES = True
JWT_TOKEN_CONFIG.JWT_COOKIE_CSRF_PROTECT = False


class RedisConfig:
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    TOKEN_BLOCKED = int(os.getenv("TOKEN_BLOCKED_REDIS_DB"))


DATABASE_SYNC_ENGINE_CONFIG = {
    "echo": True if MODE != "PROD" else False,
    "pool_size": 5,
    "max_overflow": 10,
}

DATABASE_ASYNC_ENGINE_CONFIG = {
    "echo": True if MODE != "PROD" else False,
    "pool_size": 5,
    "max_overflow": 10,
}


class PasswordValidateParams:
    special_sym: list = ["$", "@", "#", "%", "&", "*", "!"]
    min_length: int = 8
    max_length: int = 24
    one_digit_is_required: bool = True
    one_upper_is_required: bool = True
    one_lower_is_required: bool = True


class AccessSettingsDB:
    __DB_HOST: str
    __DB_PORT: int
    __DB_USER: str
    __DB_PASS: str
    __DB_NAME: str

    def __init__(self):
        self.__DB_HOST = os.getenv("DB_HOST")
        self.__DB_PORT = int(os.getenv("DB_PORT"))
        self.__DB_USER = os.getenv("DB_USER")
        self.__DB_PASS = os.getenv("DB_PASS")
        self.__DB_NAME = os.getenv("DB_NAME")

    @property
    def DB_NAME(self):
        return self.__DB_NAME

    @property
    def DATABASE_URL_ASYNCPG(self):
        return f"postgresql+asyncpg://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}"

    @property
    def DATABASE_URL_PSYCOPG(self):
        return f"postgresql+psycopg://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}"


access_settings_db = AccessSettingsDB()
