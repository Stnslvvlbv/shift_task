from fastapi import HTTPException

from config import JWT_TOKEN_CONFIG
from src.errors.error_code import ErrorCode, ErrorType


class BaseExceptions:
    code: str
    error_type: str
    status_code: int
    part: list

    def to_exception(self, field_name: str, msg, input_value=None):
        error = {
            "loc": [*self.part, field_name],
            "msg": msg,
            "type": f"{self.error_type}.{self.code}",
        }
        if input_value:
            error["input"]: input_value

        raise HTTPException(status_code=self.status_code, detail=[error])


class FieldExceptions(BaseExceptions):

    def __init__(self, error_code: ErrorCode):
        self.code = error_code.code
        self.error_type = ErrorType.VALUE_ERROR
        self.status_code = error_code.status
        self.part = [
            "body",
        ]


class LoginExceptions(BaseExceptions):

    def __init__(self, error_code: ErrorCode):
        self.code = error_code.code
        self.error_type = ErrorType.UNAUTHORIZED
        self.status_code = error_code.status
        self.part = ["body"]


class TokenExceptions(BaseExceptions):
    def __init__(self, error_code: ErrorCode):
        self.code = error_code.code
        self.error_type = ErrorType.UNAUTHORIZED
        self.status_code = error_code.status
        self.part = JWT_TOKEN_CONFIG.JWT_TOKEN_LOCATION
