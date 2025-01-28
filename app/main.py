import asyncio
from fastapi import FastAPI
from fastapi import WebSocket
from app.graphql import schema
from app.routes import broadcast_updates
from contextlib import asynccontextmanager
from strawberry.fastapi import GraphQLRouter
from app.routes import rest_router, websocket_endpoint

# Lifespan handler to manage startup and shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for managing app startup and shutdon
    """
    # Startup tasks (eg. start Websocket broadcasting task)
    task = asyncio.create_task(broadcast_updates())
    print("Background WebSocket broadcasting task started.")
    yield # application runs during this period
    # shutdown task
    task.cancel()
    print("Background WebSocket broadcasting task stopped.")

app = FastAPI(lifespan=lifespan) # Initialize FastAPI app

# REST endpoints
app.include_router(rest_router)

"""
This file is important because we want to set /graphql as the 
endpoint for all GraphQL queries and mutations.
"""
grapql_app = GraphQLRouter(schema)
app.include_router(grapql_app, prefix="/graphql") # Add GraphQL endpoint at /graphql

"""Websockets"""
@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)