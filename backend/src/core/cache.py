import redis
import logging
from typing import Optional, Any
from src.core.config import settings

logger = logging.getLogger("lablex.cache")

class RedisCache:
    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self.pool: Optional[redis.ConnectionPool] = None
        self.initialize()

    def initialize(self):
        try:
            self.pool = redis.ConnectionPool.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                max_connections=50
            )
            self.client = redis.Redis(connection_pool=self.pool)
            # Test connection
            self.client.ping()
            logger.info("Successfully connected to Redis.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis at {settings.REDIS_URL}: {e}")
            self.client = None
            self.pool = None

    def get_client(self) -> Optional[redis.Redis]:
        if not self.client:
            self.initialize()
        return self.client

    def get(self, key: str) -> Optional[str]:
        client = self.get_client()
        if not client:
            return None
        try:
            return client.get(key)
        except Exception as e:
            logger.error(f"Redis get error for key {key}: {e}")
            return None

    def set(self, key: str, value: str, expire_seconds: Optional[int] = None) -> bool:
        client = self.get_client()
        if not client:
            return False
        try:
            if expire_seconds:
                client.setex(key, expire_seconds, value)
            else:
                client.set(key, value)
            return True
        except Exception as e:
            logger.error(f"Redis set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        client = self.get_client()
        if not client:
            return False
        try:
            client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error for key {key}: {e}")
            return False

    def get_manifest_key(self, tenant_id: str, kind: str, manifest_id: str) -> str:
        return f"lablex:manifest:{tenant_id}:{kind}:{manifest_id}"

    def get_concurrent_runs_key(self, tenant_id: str) -> str:
        return f"lablex:quota:concurrent:{tenant_id}"

    def get_rate_limit_key(self, tenant_id: str, timestamp_bucket: int) -> str:
        return f"lablex:rate_limit:{tenant_id}:{timestamp_bucket}"

cache = RedisCache()
