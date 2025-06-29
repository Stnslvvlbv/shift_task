import datetime
from typing import Annotated

from sqlalchemy import BIGINT, TIMESTAMP, String, create_engine, text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import (DeclarativeBase, Session, mapped_column,
                            sessionmaker)

from config import (DATABASE_ASYNC_ENGINE_CONFIG, DATABASE_SYNC_ENGINE_CONFIG,
                    access_settings_db)

sync_engine = create_engine(
    url=access_settings_db.DATABASE_URL_PSYCOPG, **DATABASE_SYNC_ENGINE_CONFIG
)

async_engine = create_async_engine(
    url=access_settings_db.DATABASE_URL_ASYNCPG, **DATABASE_ASYNC_ENGINE_CONFIG
)

session_factory = sessionmaker(sync_engine, expire_on_commit=False, class_=Session)
async_session_factory = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


intPk = Annotated[int, mapped_column(primary_key=True)]

str_256 = Annotated[str, 256]
str_128 = Annotated[str, 128]
str_32 = Annotated[str, 32]

bool_default_false = Annotated[bool, mapped_column(default=False, nullable=True)]

created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow
    ),
]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(200),
        intPk: BIGINT,
        created_at: TIMESTAMP,
        updated_at: TIMESTAMP,
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        if len(cols) < len(self.__table__.columns):
            cols.append(" ...  ")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
