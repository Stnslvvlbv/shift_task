from enum import StrEnum


class ErrorType(StrEnum):
    VALUE_ERROR = "value_error"
    NOT_UNIQUE_VALUE = "not_unique_value"
    UNAUTHORIZED = "unauthorized"
    MISSING_FIELD = "missing_field"
    INVALID_CREDENTIALS = "invalid_credentials"
    USER_ALREADY_EXISTS = "user_already_exists"


class ErrorCode:

    def __init__(self, code, status_code):
        self.status = status_code
        self.code = code
