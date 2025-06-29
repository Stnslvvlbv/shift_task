import pytest
from sqlalchemy import text


class TestConnectDB:
    @staticmethod
    def test_sync_connect_db(sync_connection):
        """
        Тест синхронного подключения к базе данных.
        """
        result = sync_connection.execute(text("SELECT VERSION()"))
        response = result.scalar()
        assert "PostgreSQL" in response

    @staticmethod
    @pytest.mark.asyncio
    async def test_async_connect_db(async_connection):
        result = await async_connection.execute(text("SELECT VERSION()"))
        response = result.scalar()
        assert "PostgreSQL" in response
