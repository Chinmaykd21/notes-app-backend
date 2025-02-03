# app/routes/__init__.py
from .rest import router as rest_router
from .websocket import websocket_endpoint, websocket_router

__all__ = ["rest_router", "websocket_endpoint", "websocket_router"]

"""
Expose commonly used objects like routers for REST and WEBSOCKETs
to simplify main.py
"""