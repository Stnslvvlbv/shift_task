from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db.database import session_factory
from src.user.models import UserORM
from tests.dataset.user_data import users_list
from tests.dataset.position_data import positions, user_positions
from tests.db_setter.user_creater import create_test_user_sync
from tests.db_setter.position_creater import insert_position, insert_user_position
from tests.db_setter.salary_creater import insert_salary_increase


class DataControlSimple:
    def __init__(self):
        self.position_added = False
        self.user_positions_added = False
        self.salary_increase_added = False


data_control = DataControlSimple()


def populate_db_with_mock_data():
    """
    Заполняет базу данных моковыми данными через синхронную сессию.
    Игнорирует ошибки уникальности для предотвращения сбоев при повторном запуске.
    """
    try:
        # Создаем пользователей
        with session_factory() as session:
            for user_data in users_list:
                try:
                    create_test_user_sync(session, user_data)
                except IntegrityError:
                    print(f"Пользователь с email '{user_data['email']}' уже существует. Пропускаем...")
                    session.rollback()
                    continue

            session.commit()

        # Вставляем должности
        try:
            insert_position(session_factory, data_control)
        except IntegrityError:
            print("Должности уже существуют в базе данных. Пропускаем...")
            session_factory().rollback()

        # Находим пользователя по email "auth_user@gmail.com"
        with session_factory() as session:
            auth_user = session.query(UserORM).filter_by(email="auth_user@gmail.com").first()
            if not auth_user:
                raise ValueError("Пользователь с email 'auth_user@gmail.com' не найден в базе данных!")

            user_uuid = str(auth_user.id)  # Получаем UUID пользователя

        # Вставляем связи пользователь-должность
        try:
            insert_user_position(user_uuid, session_factory, data_control)
        except IntegrityError:
            print("Связи пользователь-должность уже существуют в базе данных. Пропускаем...")
            session_factory().rollback()

        # Вставляем повышения зарплаты
        try:
            insert_salary_increase(session_factory, data_control)
        except IntegrityError:
            print("Повышения зарплаты уже существуют в базе данных. Пропускаем...")
            session_factory().rollback()

        print("База данных заполнена моковыми данными!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session_factory().rollback()


if __name__ == "__main__":
    populate_db_with_mock_data()