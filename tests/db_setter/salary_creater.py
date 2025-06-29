from sqlalchemy import text

from src.salary.models import DiscussionOfSalaryIncreaseORM
from tests.dataset.salary_data import discussions


def insert_salary_increase(session_test, data_control):

    if not data_control.salary_increase_added:

        with session_test() as conn:
            for discussion in discussions:
                new_discussion = DiscussionOfSalaryIncreaseORM(
                    user_position_id=4, **discussion
                )
                conn.add(new_discussion)
            conn.query(
                text(
                    "SELECT setval('public.salary_increase_id_seq', (SELECT MAX(id) FROM salary_increase));"
                )
            )
            conn.commit()
        data_control.salary_increase_added = True

    return discussions
