from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class GeneralErrorCode:
    SERVICE_UNAVAILABLE = {
        "status_code": 503,
        "detail": "the service is temporarily unavailable",
    }


class ServiceError:

    @staticmethod
    def not_found():
        raise HTTPException(
            status_code=404, detail="data matching your request was not found"
        )
