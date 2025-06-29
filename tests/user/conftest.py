from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from db.session import get_db
from main import app
from tests.conftest import _get_test_db


@pytest.fixture(scope="function")
def valid_user_data():
    return {
        "email": "valid@test.com",
        "password": "Password123!",
        "first_name": "Иван",
        "last_name": "Иванов",
        "birth_date": "2000-01-01"
    }


@pytest.fixture(scope="function")
async def client_invalid_tokens() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_db] = _get_test_db
    cookies = {
        "refresh_token_cookie": "invalid_token",
        "access_token_cookie": "invalid_token",
    }
    with TestClient(app, cookies=cookies) as client:
        yield client
