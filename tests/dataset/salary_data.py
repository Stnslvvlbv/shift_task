from datetime import datetime, timedelta

from src.salary.models import ReviewStatusType

# Генерация времени запроса в прошлом
past_time_1 = datetime.utcnow() - timedelta(days=30)  # 30 дней назад
past_time_2 = datetime.utcnow() - timedelta(days=60)  # 60 дней назад

discussions = [
    {
        "id": 1,
        "requested_salary": 160_000.00,
        "approved_salary": None,
        "request_datetime": datetime.utcnow() - timedelta(days=60),
        "status": ReviewStatusType.REJECTED,
        "reasons_increase": "Индексация в связи с ростом инфляции.",
        "motivation_decision": "Запрос отклонен из-за недостаточной аргументации.",
    },
    {
        "id": 2,
        "requested_salary": 155_000.00,
        "approved_salary": 145_000.00,
        "request_datetime": datetime.utcnow() - timedelta(days=30),
        "status": ReviewStatusType.APPROVED,
        "reasons_increase": "Повышение заработной платы в связи с ростом квалификации",
        "motivation_decision": "Увеличение зарплаты одобрено с учетом роста квалификации.",
    },
    {
        "id": 3,
        "requested_salary": 170_000.00,
        "approved_salary": None,
        "request_datetime": datetime.utcnow() + timedelta(days=15),
        "status": ReviewStatusType.PENDING,
        "reasons_increase": "Запрос на повышение зарплаты в связи с увеличением объема работы.",
        "motivation_decision": None,
    },
]