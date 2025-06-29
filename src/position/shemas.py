from datetime import date
from typing import Optional

from src.schemas_base import TunedModel


class UserPositionSchema(TunedModel):

    position_id: int
    assigned_salary: float
    assigned_at: date
    removed_at: Optional[date] = None
