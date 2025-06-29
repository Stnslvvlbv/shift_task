from src.errors.error_code import ErrorCode


class FieldCodeExceptions:

    EMAIL_INVALID_SYNTAX = ErrorCode(status_code=400, code="email_invalid_syntax")
    EMAIL_NOT_UNIQUE = ErrorCode(status_code=409, code="email_not_unique")

    PASSWORD_TOO_SIMPLE = ErrorCode(status_code=422, code="password_too_simple")
    REQUIRED_FIELD = ErrorCode(status_code=422, code="required_field")
    LETTERS_ONLY = ErrorCode(status_code=422, code="letters_only")
    VALUE_TOO_LONG = ErrorCode(status_code=422, code="value_to_long")
    TOO_YOUNG_AGE = ErrorCode(status_code=422, code="too_young_age")


class ServiceAuthException:
    UNKNOWING_EMAIL = ErrorCode(status_code=401, code="email_not_registered")
    PASSWORD_INVALID = ErrorCode(status_code=401, code="password_invalid")
    MISSING_TOKEN = ErrorCode(status_code=400, code="missing_token")
    TOKEN_INVALID = ErrorCode(status_code=401, code="token_invalid")
    ACCESS_RESTRICTION = ErrorCode(status_code=403, code="access_restriction")
