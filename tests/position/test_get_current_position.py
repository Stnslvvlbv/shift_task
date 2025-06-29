from sqlalchemy import text


def test_position_success(inserted_user_positions, client_for_active_user):
    """
    Тест успешного получения должности пользователя
    """

    response = client_for_active_user.get("/position/current")

    assert response.status_code == 200
    assert "assigned_salary" in response.json()


def test_non_active_user(inserted_user_positions, client_for_non_active_user):
    """
    Тест отказа в доступе для не активного пользователя
    """

    response = client_for_non_active_user.get("/position/current")

    assert response.status_code == 403
    assert response.json()["detail"][0]["type"] == "unauthorized.access_restriction"


def test_user_is_active_by_token_but_non_active_in_db(inserted_user_positions, client_for_active_user, session_test):

    response = client_for_active_user.get("/user")

    assert response.status_code == 200
    assert "id" in response.json()

    # Получаем user_uuid из ответа
    user_uuid = response.json()["id"]

    # Обновляем поле is_active = False для пользователя в базе данных
    with session_test() as conn:
        conn.execute(
            text("UPDATE \"user\" SET is_active = FALSE WHERE id = :user_uuid"),
            {"user_uuid": user_uuid},
        )
        conn.commit()

    response_after_update = client_for_active_user.get("/position/current")

    # Проверяем, что теперь данные не доступны пользователю, если access токен еще не обновлен
    assert response_after_update.status_code == 404

    # Возвращаем все как было для последующих тестов
    with session_test() as conn:
        conn.execute(
            text("UPDATE \"user\" SET is_active = TRUE WHERE id = :user_uuid"),
            {"user_uuid": user_uuid},
        )
        conn.commit()