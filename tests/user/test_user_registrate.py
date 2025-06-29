import json


def test_successful_registration(client):
    """
    Проверяет успешную регистрацию пользователя
    """
    data = {
        "email": "new_user@example.com",
        "password": "Password123#",
        "first_name": "Иван",
        "last_name": "Иванов",
        "middle_name": "Иванович",
        "birth_date": "2000-01-01",
    }

    response = client.post("/user/registrate", data=json.dumps(data))

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == data["email"]


async def test_register_duplicate_email(client):
    """
    Проверяет, что нельзя зарегистрироваться с существующим email
    """
    data = {
        "email": "duplicate@example.com",
        "password": "Password123@",
        "first_name": "Петр",
        "last_name": "Петров",
        "middle_name": "Петрович",
        "birth_date": "2000-01-01",
    }

    # Первый запрос — успешный
    first_response = client.post("/user/registrate", json=data)
    assert first_response.status_code == 200

    second_response = client.post("/user/registrate", json=data)
    assert second_response.status_code == 409
