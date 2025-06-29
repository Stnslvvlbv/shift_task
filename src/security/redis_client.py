from redis import Redis
from redis.connection import BlockingConnectionPool

from config import RedisConfig

pool = BlockingConnectionPool(max_connections=25, timeout=5)
redis_client = Redis(
    host=RedisConfig.REDIS_HOST,
    port=RedisConfig.REDIS_PORT,
    db=RedisConfig.TOKEN_BLOCKED,
    decode_responses=True,
    connection_pool=pool,
)
