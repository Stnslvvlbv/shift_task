import datetime
from pydantic import BaseModel


class TunedModel(BaseModel):

    class Config:
        """tells pydentic to convert even non dict obj to json"""

        from_attributes = True  # Для работы с ORM SQLAlchemy
        json_encoders = {  # Настройка сериализации datetime
            datetime: lambda dt: dt.isoformat()
        }
