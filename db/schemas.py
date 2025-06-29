from enum import Enum
from typing import Optional

from fastapi import HTTPException
from fastapi.params import Query
from pydantic import BaseModel, validator

from config import MAX_LIMIT_PAGINATE


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class PaginationSchemas(BaseModel):
    """
    Схема для параметров пагинации.
    """

    limit: int = Query(15, ge=1, le=MAX_LIMIT_PAGINATE)
    offset: int = Query(0, ge=0)

    @validator("limit")
    def validate_limit(cls, value):
        if value > MAX_LIMIT_PAGINATE:
            raise HTTPException(
                status_code=422,
                detail=f"Превышено максимальное количество записей {MAX_LIMIT_PAGINATE}",
            )

        return value


class SortingSchemas(BaseModel):
    """
    Схема для параметров сортировки.
    """

    sort_by: Optional[str] = None
    sort_order: Optional[SortOrder] = SortOrder.ASC


class PaginationSortingSchemas(PaginationSchemas, SortingSchemas):
    """
    Объединённая схема для параметров пагинации и сортировки.
    """

    pass


class PaginationSortingResponseSchemas(PaginationSortingSchemas):
    count: int
