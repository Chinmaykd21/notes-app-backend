# app/routes/__init__.py
from .rest import router as rest_router
from .websocket import websocket_endpoint, broadcast_updates

__all__ = ["rest_router", "websocket_endpoint", "broadcast_updates"]

"""
Expose commonly used objects like routers for REST and WEBSOCKETs
to simplify main.py
"""