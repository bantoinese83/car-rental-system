# app/utils/cache.py
import json

from app.core.redis_config import redis_client


def get_cache(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None


def set_cache(key: str, value: dict, expire: int = 3600):
    redis_client.set(key, json.dumps(value), ex=expire)


def delete_cache(key: str):
    redis_client.delete(key)
