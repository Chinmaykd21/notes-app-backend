import os
from redis import Redis

# Use environment variables for Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def publish(channel: str, message: str):
    print(f"channel - {channel}, message - {message}")
    redis.publish(channel, message)

def subscribe(channel: str):
    pubsub = redis.pubsub()
    pubsub.subscribe(channel)
    print(f"subscribing to {channel}, pubsub - {pubsub}")
    return pubsub