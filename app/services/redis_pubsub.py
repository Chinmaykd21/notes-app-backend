import os
import json
import asyncio
from redis.asyncio import Redis, ConnectionPool
from asyncio import Queue

# Use environment variables for Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_CHANNEL_PREFIX = "note"


"""
    Benefits of this approach:
        1. Improves performance (no need to establish a new connection every time)
        2. Reduces Redis overhead (connections are reused)
        3. Handle high concurrency better
"""
# Initialize Redis connection pool
redis_pool = ConnectionPool.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
redis = Redis(connection_pool=redis_pool, decode_responses=True)

def publish(channel: str, message: str):
    redis.publish(channel, message)

def subscribe(channel: str):
    pubsub = redis.pubsub()
    pubsub.subscribe(channel)
    return pubsub

async def subscribe_to_note_channel(redis, note_id:str):
    """
        subscribe to Redis channel for a specific note
    """
    channel = f"{REDIS_CHANNEL_PREFIX}:{note_id}"
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)
    return pubsub

async def batch_publish(redis, note_id: str, queue: Queue, batch_interval: float = 0.2):
    """
        Batch redis messages before publishing.
        Collects all messages from a queue and publishes them in a single batch
    """
    channel = f"{REDIS_CHANNEL_PREFIX}:{note_id}"
    while True:
        await asyncio.sleep(batch_interval)
        messages = []
        while not queue.empty():
            messages.append(await queue.get())

        if messages:
            message = { "updates": messages }
            # ✅ Convert dict to JSON string
            # We do this since redis does not accept dictionary directly.
            # We have to convert this to JSON strings
            message_json = json.dumps(message)
            print(f"📢 Publishing to Redis channel {channel}: {message_json}") 
            await redis.publish(channel, message_json)