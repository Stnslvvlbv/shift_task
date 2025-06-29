from logging import getLogger
from typing import Callable

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse

from config import MODE


class LoggingOrError:
    def __init__(self):
        self.base_logging = getLogger(__name__)

    def _log_or_raise(
        self, log_method, message, exception_message=None, exc_info=False
    ):
        """
        Helper method to either log the message or raise an exception based on MODE
        """
        if MODE == "PROD":
            log_method(message, exc_info=exc_info)
        else:
            raise ValueError(exception_message or message)

    def error(self, message):
        """
        Логирует или выбрасывает ValueError.
        """
        self._log_or_raise(self.base_logging.error, message, message, exc_info=True)

    def info(self, message):
        """
        Логирует информацию или выбрасывает ValueError.
        """
        self._log_or_raise(self.base_logging.info, message, message)


# Create a global logger instance
logger = LoggingOrError()


async def error_middleware(request: Request, call_next: Callable) -> Response:
    try:
        return await call_next(request)
    except HTTPException as exc:
        # Логируем деталь ошибки
        if isinstance(exc.detail, dict):
            detail = exc.detail.get("detail", "Unknown error")
        else:
            detail = exc.detail

        logger.error(f"HTTPException: {detail}")

        # Необходимая мера, так как внутри HTTPException не содержися raise
        return HTTPException(**exc)

    except Exception as exc:
        # Логируем полный traceback
        logger.error(f"Unexpected error: {str(exc)}")

        return JSONResponse(
            status_code=500,
            content={
                "detail": {
                    "code": 500,
                    "message": "Internal Server Error",
                    "details": str(exc) if MODE != "PROD" else None,
                }
            },
        )
