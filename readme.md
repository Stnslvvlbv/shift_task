# Shift Task — REST API для просмотра зарплаты с JWT-авторизацией

Этот проект представляет собой REST API для просмотра информации о зарплате сотрудников с использованием JWT-токенов для авторизации.

---

## Функционал

- Регистрация и вход пользователей
- JWT-авторизация
- Просмотр данных пользователя
- Просмотр должности пользователя и текущей заработной платы
- Просмотр информации о грядущих рассмотрениях повышения заработной платы
- Поддержка PostgreSQL и Redis
- Тесты (pytest)

---

## Технологии

- Python 3.13
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Pydantic
- AuthX / AuthX Extra
- Poetry
- Docker / Docker Compose

---

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://gitlab.com/stnslvvlbv/shift_task.git
cd shift_task
```
### 2. При необходимости установите Poetry
```bash
pip install poetry
```
### 3. Установите зависимости через Poetry
```bash
poetry install
```
### 4.  Создайте .env и docker-compose.yml из примера
```bash
cp .example.env .env
cp docker-compose.example.yml docker-compose.yml
```
*При необходимости отредактируйте .env и docker-compose.yml, чтобы указать свои настройки БД, Redis и секретные ключи.*
### 5. Запустите инфраструктуру через Docker Compose
```bash
docker-compose up -d
```
### 6. Примените миграции
```bash
poetry run alembic upgrade head
```
### 7. Запустите сервер
```bash
poetry run uvicorn main:app --reload
```
*Сервис будет доступен по адресу: http://localhost:8000*

---
## Запуск тестов
```bash
poetry run pytest
```
---
## Демонстрация
Сервис использует две базы данных, развернутых в docker. Боевую и для тестирования.
Для простоты демонстрации работы сервиса реализована возможность заполнение "боевой"
базы данных демонстрационными данными. Если Вам это потребуется:
```bash
poetry run python populate_data.py
```
Документация API доступна по ссылке http://127.0.0.1:8000/docs
или http://127.0.0.1:8000/redoc в зависимости от предпочтений.
Доступ к данным пользователя с демонстрационными данными по:

 - **username:**   `auth_user@gmail.com`
 - **password:**   `#Password1`
### Полная отчистка базы данных
```bach
poetry run alembic downgrade base
poetry run alembic upgrade head
```