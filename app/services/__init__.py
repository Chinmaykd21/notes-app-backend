# app/services/__init__.py
from .websocket_manager import remove_client, add_client, connected_clients

__all__ = ["remove_client", "add_client", "connected_clients"]

"""
Expose reusable utilities like redis so they can be imported in main.py
"""