import json


def test_login_user_success(client):
    user_data = {
        "email": "gagarina@test.com",
        "password": "1qwedcxzA*&#",
        "first_name": "Проверяющий",
        "middle_name": "Успешную",
        "last_name": "Аутентификацию",
        "birth_date": "1998-06-24",
    }
    form_data = {
        "username": user_data["email"],
        "password": user_data["password"],
    }

    resp_create = client.post("/user/registrate/", data=json.dumps(user_data))
    assert resp_create.status_code == 200
    resp_login = client.post(
        "/user/login/",
        data=form_data,
    )
    assert resp_login.status_code == 200
    assert resp_login.cookies["access_token_cookie"]
    assert resp_login.cookies["refresh_token_cookie"]


def test_wrong_password(client):
    user_data = {
        "email": "urgant@test.com",
        "password": "1qwedcxzA*&#",
        "first_name": "Проверяющий",
        "middle_name": "Ошибочный",
        "last_name": "Пароль",
        "birth_date": "1998-06-24",
    }
    form_data = {
        "username": user_data["email"],
        "password": user_data["password"] + "_wrong",
    }

    resp_create = client.post("/user/registrate/", data=json.dumps(user_data))
    assert resp_create.status_code == 200
    resp_login = client.post(
        "/user/login/",
        data=form_data,
    )
    assert resp_login.status_code == 401


def test_wrong_email(client):
    user_data = {
        "email": "volya@test.com",
        "password": "1qwedcxzA*&#",
        "first_name": "Проверяющий",
        "middle_name": "Ошибочный",
        "last_name": "Емаил",
        "birth_date": "1998-06-24",
    }
    form_data = {
        "username": "wrong_" + user_data["email"],
        "password": user_data["password"],
    }

    resp_create = client.post("/user/registrate/", data=json.dumps(user_data))
    assert resp_create.status_code == 200
    resp_login = client.post(
        "/user/login/",
        data=form_data,
    )
    assert resp_login.status_code == 401
