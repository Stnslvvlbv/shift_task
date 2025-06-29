import datetime
import re
import uuid

from email_validator import EmailNotValidError, validate_email
from pydantic import EmailStr, Field, field_validator

from src.errors.http_value_exception import FieldExceptions
from src.errors.type_error_ import FieldCodeExceptions
from src.schemas_base import TunedModel
from src.user.validate import password_mach_pattern

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserRegistrateSchema(TunedModel):
    email: str
    password: str = Field(
        description="Пароль должен быть длиннее 8 символов, короче 24 символов, включать заглавные и строчные буквы, а также цифры и специальные символы ($, @, #, %, &, *)"
    )
    first_name: str
    middle_name: str | None = None
    last_name: str
    birth_date: datetime.date

    @field_validator("password")
    def validating_password(cls, value, info):
        err = password_mach_pattern(value)
        if err:
            raise FieldExceptions(FieldCodeExceptions.PASSWORD_TOO_SIMPLE).to_exception(
                info.field_name, err, value
            )
        return value

    @field_validator("email")
    def validating_email(cls, value, info):
        try:
            email_info = validate_email(value, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as err:
            raise FieldExceptions(
                FieldCodeExceptions.EMAIL_INVALID_SYNTAX
            ).to_exception(info.field_name, f"{err}", value)
        return email

    @field_validator("first_name", "last_name")
    def required_field(cls, value, info):
        if not value:
            raise FieldExceptions(FieldCodeExceptions.REQUIRED_FIELD).to_exception(
                info.field_name, "the field is required", value
            )
        return value

    @field_validator("first_name", "last_name", "middle_name")
    def validating_names(cls, value, info):
        max_len = 32

        if not LETTER_MATCH_PATTERN.match(value) and len(value) > 0:
            raise FieldExceptions(FieldCodeExceptions.REQUIRED_FIELD).to_exception(
                info.field_name,
                "the field must contain only Cyrillic or Latin letters",
                value,
            )

        if len(value) > max_len:
            raise FieldExceptions(FieldCodeExceptions.VALUE_TOO_LONG).to_exception(
                info.field_name,
                f"the field must not exceed {max_len} characters",
                value,
            )

        return value

    @field_validator("birth_date")
    def validating_age(cls, value, info):
        today = datetime.date.today()
        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )
        if age < 18:
            raise FieldExceptions(FieldCodeExceptions.TOO_YOUNG_AGE).to_exception(
                info.field_name, "User must be over 18 years old", value
            )
        return value


class UserShowSchema(TunedModel):

    id: uuid.UUID
    email: EmailStr
    first_name: str
    middle_name: str | None = None
    last_name: str
    birth_date: datetime.date
    created_at: datetime.datetime
    is_active: bool = True


class UserAuthDTOSchema(TunedModel):
    id: uuid.UUID
    email: EmailStr
    registered_at: datetime.datetime
    is_active: bool = True


class UserDataFromTokenSchema(TunedModel):
    is_active: bool = True
