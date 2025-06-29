# Shift Task — REST API для просмотра зарплаты с JWT-авторизацией

Этот проект представляет собой REST API для просмотра информации о зарплате сотрудников с использованием JWT-токенов для авторизации.

---

## Функционал

- Регистрация и вход пользователей
- Просмотр данных о своей зарплате
- JWT-авторизация
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

## 🔧 Установка и запуск

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
При необходимости отредактируй .env и docker-compose.yml чтобы указать свои настройки БД, Redis и секретные ключи. 