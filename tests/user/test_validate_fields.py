import pytest
import datetime
from fastapi import HTTPException
from src.user.schemas import UserRegistrateSchema


def test_password_too_short(valid_user_data):
    valid_user_data['password'] = "Short1!"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "Length should be at least 8." in exc_info.value.detail[0]["msg"]


def test_password_missing_special_char(valid_user_data):
    valid_user_data['password'] = "Password123"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "one of the symbols $, @, #, %, &, *" in exc_info.value.detail[0]["msg"]


def test_password_missing_numeral(valid_user_data):
    valid_user_data['password'] = "Password!"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "Password should have at least one numeral." in exc_info.value.detail[0]["msg"]


def test_password_missing_uppercase_letter(valid_user_data):
    valid_user_data['password'] = "password1!"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "Password should have at least one uppercase letter." in exc_info.value.detail[0]["msg"]


def test_password_missing_lowercase_letter(valid_user_data):
    valid_user_data['password'] = "@PASSWORD1"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "Password should have at least one lowercase letter." in exc_info.value.detail[0]["msg"]


def test_password_missing_too_long(valid_user_data):
    valid_user_data['password'] = "@PASSWORD1" + "a" * 15
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "Length should be not be greater than 24." in exc_info.value.detail[0]["msg"]


def test_first_name_with_numbers(valid_user_data):
    valid_user_data['first_name'] = "Иван123"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "the field must contain only Cyrillic or Latin letters" in exc_info.value.detail[0]["msg"]


def test_first_name_too_long(valid_user_data):
    valid_user_data["first_name"] = "A" * 33
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "must not exceed 32 characters" in exc_info.value.detail[0]["msg"]


def test_email_not_contain_at(valid_user_data):
    valid_user_data['email'] = "new_userexample.com"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 400
    assert "An email address must have an @-sign." in exc_info.value.detail[0]["msg"]


def test_email_not_contain_period(valid_user_data):
    valid_user_data['email'] = "new_user@examplecom"
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 400
    assert "The part after the @-sign is not valid. It should have a period." in exc_info.value.detail[0]["msg"]


def test_first_name_empty_sting(valid_user_data):
    valid_user_data["first_name"] = ""
    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "the field is required" in exc_info.value.detail[0]["msg"]


def test_user_underage(valid_user_data):
    today = datetime.date.today()
    underage_birthdate = today.replace(year=today.year - 17, month=1, day=1)
    valid_user_data["birth_date"] = underage_birthdate

    with pytest.raises(HTTPException) as exc_info:
        UserRegistrateSchema(**valid_user_data)

    assert exc_info.value.status_code == 422
    assert "User must be over 18 years old" in exc_info.value.detail[0]["msg"]