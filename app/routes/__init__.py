# app/routes/__init__.py
from .rest import router as rest_router

__all__ = ["rest_router"]

"""
Expose commonly used objects like routers for REST and WEBSOCKETs
to simplify main.py
"""