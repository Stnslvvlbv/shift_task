from sqlalchemy import text


def test_salary_increase_success(inserted_salary_increase, client_for_active_user):
    """
    Тест успешного получения должности пользователя
    """

    response = client_for_active_user.get("/salary/future_increase")

    assert response.status_code == 200
    assert "request_datetime" in response.json()[0]


def test_get_salary_increase_non_active_user(inserted_user_positions, client_for_non_active_user):
    """
    Тест отказа в доступе для не активного пользователя
    """

    response = client_for_non_active_user.get("/salary/future_increase")

    assert response.status_code == 403
    assert response.json()["detail"][0]["type"] == "unauthorized.access_restriction"