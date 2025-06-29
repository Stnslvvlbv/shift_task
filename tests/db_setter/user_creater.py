from sqlalchemy.orm import Session

from src.security.hasher import Hasher
from src.user.models import UserORM


def create_test_user_sync(session: Session, user_data: dict) -> UserORM:
    """
    Создает нового пользователя в базе данных (синхронная версия).
    """
    hash_password = Hasher.get_password_hash(user_data["password"])
    new_user = UserORM(
        email=user_data["email"],
        first_name=user_data["first_name"],
        middle_name=user_data["middle_name"],
        last_name=user_data["last_name"],
        birth_date=user_data["birth_date"],
        hash_password=hash_password,
        is_active=user_data["is_active"],
    )
    session.add(new_user)
    session.flush()  # Обновляем объект для получения ID
    return new_user
