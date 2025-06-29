from datetime import date

positions = [
    {
        "id": 1,
        "name": "Junior Software Developer",
        "description": "Начинающий разработчик программного обеспечения. Работает под руководством старших разработчиков, пишет код, исправляет ошибки и участвует в тестировании.",
        "min_salary": 40_000.00,
        "max_salary": 80_000.00,
    },
    {
        "id": 2,
        "name": "Senior DevOps Engineer",
        "description": "Опытный инженер DevOps. Отвечает за автоматизацию процессов развертывания, управление инфраструктурой как кодом (IaC) и обеспечение бесперебойной работы систем.",
        "min_salary": 120_000.00,
        "max_salary": 180_000.00,
    },
    {
        "id": 3,
        "name": "Data Scientist",
        "description": "Специалист по анализу данных. Разрабатывает модели машинного обучения, проводит исследование больших данных и предоставляет аналитические отчеты для бизнеса.",
        "min_salary": 90_000.00,
        "max_salary": 150_000.00,
    },
    {
        "id": 4,
        "name": "UI/UX Designer",
        "description": "Дизайнер пользовательского интерфейса и опыта. Создает прототипы интерфейсов, проводит исследования пользователей и улучшает удобство использования продукта.",
        "min_salary": 70_000.00,
        "max_salary": 110_000.00,
    },
    {
        "id": 5,
        "name": "Cybersecurity Specialist",
        "description": "Специалист по кибербезопасности. Обеспечивает защиту данных компании, выявляет уязвимости и разрабатывает стратегии защиты от атак.",
        "min_salary": 80_000.00,
        "max_salary": 140_000.00,
    },
    {
        "id": 6,
        "name": "Product Manager",
        "description": "Менеджер продукта. Отвечает за разработку стратегии продукта, координацию команды разработчиков и взаимодействие с заказчиками для достижения бизнес-целей.",
        "min_salary": 100_000.00,
        "max_salary": 160_000.00,
    }
]

user_positions = [
    {
        "id": 1,
        "position_id": 1,  # Junior Software Developer
        "assigned_salary": 60_000.00,
        "assigned_at": date(2021, 1, 15),
        "removed_at": date(2022, 1, 15),
    },
    {
        "id": 2,
        "position_id": 3,  # Data Scientist
        "assigned_salary": 100_000.00,
        "assigned_at": date(2022, 1, 15),
        "removed_at": date(2022, 6, 15),
    },
    {
        "id": 3,
        "position_id": 5,  # Cybersecurity Specialist
        "assigned_salary": 120_000.00,
        "assigned_at": date(2022, 6, 15),
        "removed_at": date(2023, 4, 15),
    },
    {
        "id": 4,
        "position_id": 2,  # Senior DevOps Engineer
        "assigned_salary": 145_000.00,
        "assigned_at": date(2023, 4, 15),
        "removed_at": None,
    },
]
