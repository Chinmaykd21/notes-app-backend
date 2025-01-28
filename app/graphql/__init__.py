# app/graphql/__init__.py
from .schema import schema
from .models import Note

__all__ = ["schema", "Note"]

"""
Expose GraphQL schema and models for easier imports in main.py
"""