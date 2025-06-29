async def test_get_user_success(client_for_active_user):
    """
    Тест успешного получения информации о пользователя.
    """
    response = client_for_active_user.get("/user")

    # Проверяем статус-код
    assert response.status_code == 200

    # Проверяем, содержание ответа
    json_data = response.json()
    assert "id" in json_data


async def test_get_user_without_access_token(client):
    """
    Тест ответа отказа в доступе без токена.
    """
    response = client.get("/user")

    # Проверяем статус-код
    assert response.status_code == 400

    # Проверяем, тип исключения
    json_data = response.json()
    assert "missing_token" in json_data["detail"][0]["type"]


async def test_get_user_invalid_access_token(client_invalid_tokens):
    """
    Тест ответа отказа в доступе без токена.
    """
    response = client_invalid_tokens.get("/user")

    # Проверяем статус-код
    assert response.status_code == 401

    # Проверяем, тип исключения
    json_data = response.json()
    assert "token_invalid" in json_data["detail"][0]["type"]
