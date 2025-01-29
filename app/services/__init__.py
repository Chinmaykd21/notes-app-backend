# app/services/__init__.py
from .redis_pubsub import redis, batch_publish, subscribe_to_note_channel
from .websocket_manager import connected_clients, broadcast, remove_client

__all__ = ["redis", "batch_publish", "subscribe_to_note_channel", "connected_clients", "broadcast", "remove_client",]

"""
Expose reusable utilities like redis so they can be imported in main.py
"""