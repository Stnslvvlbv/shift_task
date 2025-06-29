from typing import Generator, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy import desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.database import async_session_factory, Base


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session_factory()
        yield session
    finally:
        pass
        await session.close()


class BaseDAL:
    """Base class of the data access layer"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @staticmethod
    def _apply_sorting(query, sort_by: Optional[str], sort_order: str, model_orm: Base):
        """
        Применяет сортировку к запросу.

        :param query: Исходный SQL-запрос.
        :param sort_by: Поле для сортировки.
        :param sort_order: Порядок сортировки ("asc" или "desc").
        :return: Изменённый SQL-запрос с сортировкой.
        """
        if sort_by:
            # Проверяем, существует ли поле в модели PsyTestOrm
            if hasattr(model_orm, sort_by):
                column = getattr(model_orm, sort_by)
                if str(sort_order).lower() == "desc":
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(asc(column))
            else:
                raise ValueError(f"Предупреждение: Поле '{sort_by}' не найдено в модели.")
        return query

    async def _apply_pagination_and_count(
            self,
            query,
            limit: int = None,
            offset: int = None
    ) -> Tuple:
        """
        Применяет пагинацию к запросу и возвращает общий счет записей.

        :param query: Исходный SQL-запрос.
        :param limit: Максимальное количество записей на странице.
        :param offset: Смещение для текущей страницы.
        :return: Кортеж из измененного запроса с пагинацией и общего количества записей.
        """
        try:
            # Подсчитываем общее количество записей
            count_query = select(func.count()).select_from(query.subquery())
            total_count_result = await self.db_session.execute(count_query)
            total_count = total_count_result.scalar()

            # Устанавливаем значения по умолчанию, если они не заданы
            limit = limit if limit is not None else 15  # По умолчанию 15 записей на страницу
            offset = offset if offset is not None else 0  # По умолчанию смещение 0

            # Проверяем корректность параметров offset и limit
            if offset < 0 or limit <= 0:
                raise HTTPException(status_code=400, detail="Некорректные параметры offset или limit")

            if offset >= total_count > 0:
                raise HTTPException(status_code=400,
                                    detail=f"Параметр offset ({offset}) превышает количество записей ({total_count})")

            # Применяем пагинацию
            effective_limit = min(limit, total_count - offset) if total_count > offset else 0
            query = query.limit(effective_limit).offset(offset)

            return query, total_count

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # except IntegrityError as err:
        #     raise HTTPException(status_code=400, detail=str(e))


