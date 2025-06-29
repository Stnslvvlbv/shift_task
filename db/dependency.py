from fastapi import Depends

from db.schemas import (PaginationSortingResponseSchemas,
                        PaginationSortingSchemas)


def pagination_sorting_response(
    sort_paginate: PaginationSortingSchemas = Depends(),
    count: int = 0,
) -> PaginationSortingResponseSchemas:
    """
    Зависимость для преобразования параметров пагинации, сортировки и общего количества записей
    в объект PaginationSortingResponseSchemas.

    :param sort_paginate: Параметры пагинации и сортировки.
    :param count: Общее количество записей.
    :return: Объект PaginationSortingResponseSchemas.
    """

    # Установка значений по умолчанию, если они отсутствуют
    limit = sort_paginate.limit if sort_paginate.limit is not None else 15
    offset = sort_paginate.offset if sort_paginate.offset is not None else 0

    return PaginationSortingResponseSchemas(
        limit=limit,
        offset=offset,
        sort_by=sort_paginate.sort_by,
        sort_order=sort_paginate.sort_order,
        count=count,
    )
