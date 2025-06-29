from sqlalchemy import text

from src.position.models import PositionORM, UserPositionORM
from tests.dataset.position_data import positions, user_positions


def insert_position(session_test, data_control):

    if not data_control.position_added:

        with session_test() as conn:

            for pos in positions:
                new_pos = PositionORM(**pos)
                conn.add(new_pos)
            conn.query(
                text(
                    "SELECT setval('public.position_id_seq', (SELECT MAX(id) FROM position));"
                )
            )
            conn.commit()
        data_control.position_added = True

    return positions


def insert_user_position(user_uuid, session_test, data_control):

    if not data_control.user_positions_added:

        with session_test() as conn:
            for user_pos in user_positions:
                new_ser_pos = UserPositionORM(user_uuid=user_uuid, **user_pos)
                conn.add(new_ser_pos)
            conn.query(
                text(
                    "SELECT setval('public.user_position_id_seq', (SELECT MAX(id) FROM user_position));"
                )
            )
            conn.commit()
        data_control.user_positions_added = True

    return user_positions
