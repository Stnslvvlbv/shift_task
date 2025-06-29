

async def test_refresh_token_success(client_for_active_user):
    """
    Тест успешного обновления access токена.
    """
    response = client_for_active_user.post("/user/refresh")

    # Проверяем статус-код
    assert response.status_code == 200

    # Проверяем, что куки с обновленным access токеном был отправлен
    assert response.cookies["access_token_cookie"]


async def test_missing_refresh_token(client):
    """
    Тест успешного обновления access токена.
    """
    response = client.post("/user/refresh")

    # Проверяем статус-код
    assert response.status_code == 400

    # Проверяем, тип исключения
    json_data = response.json()
    assert "missing_token" in json_data["detail"][0]["type"]


async def test_invalid_refresh_token(client_invalid_tokens):
    """
    Тест успешного обновления access токена.
    """
    response = client_invalid_tokens.post("/user/refresh")

    # Проверяем статус-код
    assert response.status_code == 401

    # Проверяем, тип исключения
    json_data = response.json()
    assert json_data["detail"][0]["type"] == "unauthorized.token_invalid"
