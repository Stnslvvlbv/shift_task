from src.security.redis_client import redis_client


def test_logout_blocks_token_and_prevents_login(client_for_active_user):

    redis_client.flushall()
    # Первый вызов — успешный logout
    response = client_for_active_user.post("/user/logout/")
    assert response.status_code == 200

    # Проверяем, что токен действительно заблокирован
    assert len(redis_client.keys("*")) == 2

    # Проверяем блокировку access токена
    response_get_user = client_for_active_user.get("/user/")
    assert response_get_user.status_code == 401

    assert response_get_user.json()["detail"][0]["type"] == "unauthorized.token_invalid"

    # Проверяем блокировку refresh токена
    response_refresh = client_for_active_user.post("/user/refresh/")
    assert response_refresh.status_code == 401

    assert response_refresh.json()["detail"][0]["type"] == "unauthorized.token_invalid"

    # очищаем redis для дальнейшего использования client_for_superuser
    redis_client.flushall()
