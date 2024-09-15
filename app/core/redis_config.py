# app/core/redis_config.py
import redis as sync_redis
import redis.asyncio as aioredis
from loguru import logger

from app.core.app_config import settings

redis_client = sync_redis.Redis.from_url(settings.REDIS_URL)

# Define the global variable at the module level
async_redis = None


async def init_redis() -> None:
    global async_redis
    try:
        async_redis = aioredis.from_url(settings.REDIS_URL)
        logger.info("Redis initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing Redis: {e}")
        raise


async def get_redis() -> None:
    if async_redis is None:
        raise RuntimeError("Redis is not initialized")
    return async_redis


async def close_redis() -> None:
    global async_redis
    if async_redis is not None:
        await async_redis.close()
        logger.info("Redis connection closed.")
    else:
        logger.warning("Redis is not initialized, so it cannot be closed.")
