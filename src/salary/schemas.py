from datetime import datetime
from typing import Optional

from src.salary.models import ReviewStatusType
from src.schemas_base import TunedModel


class SalaryIncreaseSchema(TunedModel):

    requested_salary: float
    approved_salary: Optional[float] = None
    request_datetime: datetime
    status: ReviewStatusType
    reasons_increase: str
    motivation_decision: Optional[str] = None
