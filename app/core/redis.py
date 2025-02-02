from typing import Any, Optional

from loguru import logger
from redis import ResponseError, asyncio as aioredis
from redis.exceptions import ConnectionError as RedisConnectionError
from redis.exceptions import TimeoutError as RedisTimeoutError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from app.core.config import settings


REDIS_SOCKET_TIMEOUT: float = 5.0
REDIS_SOCKET_CONNECT_TIMEOUT: float = 5.0
REDIS_DEFAULT_CACHE_EXPIRATION = 3600

redis = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
    socket_timeout=REDIS_SOCKET_TIMEOUT,
    socket_connect_timeout=REDIS_SOCKET_CONNECT_TIMEOUT,
)


async def get_redis():
    return redis


async def close_redis_connection():
    await redis.close()


async def set_redis_with_retry(
    key: str, value: Any, expiration: int = REDIS_DEFAULT_CACHE_EXPIRATION
) -> bool:
    try:
        await _redis_set(key, value, expiration)
        return True
    except (RedisTimeoutError, RedisConnectionError) as e:
        logger.error(
            f"Failed to set key {key} in Redis after retries: {str(e)}"
        )  # noqa
        return False


async def get_redis_with_retry(key: str) -> Optional[str]:
    try:
        return await _redis_get(key)
    except (RedisTimeoutError, RedisConnectionError) as e:
        logger.error(
            f"Failed to get key {key} from Redis after retries: {str(e)}"
        )  # noqa
        return None


async def delete_redis_with_retry(key: str) -> Optional[str]:
    try:
        return await _redis_del(key)
    except (RedisTimeoutError, RedisConnectionError) as e:
        logger.error(
            f"Failed to delete key {key} from Redis after retries: {str(e)}"
        )  # noqa
        return False


async def flush_all_keys() -> bool:
    try:
        await _flush_db()
        return True
    except (RedisTimeoutError, RedisConnectionError, ResponseError) as e:
        logger.error(f"Failed to flush keys from Redis after retries: {str(e)}")  # noqa
        return False


#  private methods


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=5),
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    reraise=True,
)
async def _flush_db() -> None:
    await redis.flushdb()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=5),
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    reraise=True,
)
async def _redis_del(key: str) -> Optional[str]:
    result = await redis.delete(key)
    return result > 0


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=5),
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    reraise=True,
)
async def _redis_set(key: str, value: Any, expiration: int) -> None:
    await redis.set(key, value, ex=expiration)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(multiplier=1, max=5),
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    reraise=True,
)
async def _redis_get(key: str) -> Optional[str]:
    return await redis.get(key)
