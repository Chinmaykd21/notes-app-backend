import os
import json
import redis

class RedisCache:
    """
        Handles Redis caching operations.
    """
    def __init__(self):
        self.redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

    def get(self, key):
        """
            Retrieves data from Redis.
        """
        value = self.redis_client.get(key)
        return json.loads(value) if value else None

    def set(self, key, value, expire_time=300):
        """
            Stores data in Redis with expiration.
        """
        self.redis_client.set(key, json.dumps(value), ex=expire_time)

    def delete(self, key):
        """
            Deletes a key from Redis cache.
        """
        self.redis_client.delete(key)
