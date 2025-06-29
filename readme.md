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

### 1. Клонируй репозиторий

```bash
git clone https://gitlab.com/stnslvvlbv/shift_task.git
cd shift_task
```
### 2. При необходимости установи Poetry
```bash
pip install poetry
```
### 3. Установи зависимости через Poetry
```bash
poetry install
```
### 4.  Создай .env и docker-compose.yml из примера
```bash
cp .example.env .env
cp docker-compose.example.yml docker-compose.yml
```
*При необходимости отредактируй .env и docker-compose.yml, чтобы указать свои настройки БД, Redis и секретные ключи.*
### 5. Запусти инфраструктуру через Docker Compose
```bash
docker-compose up -d
```
### 6. Примени миграции
```bash
poetry run alembic upgrade head
```
### 7. Запусти сервер
```bash
poetry run uvicorn app.main:app --reload
```
*Сервис будет доступен по адресу: http://localhost:8000*

---
## Запуск тестов
```bash
poetry run pytest
```