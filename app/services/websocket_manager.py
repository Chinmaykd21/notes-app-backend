from fastapi import WebSocket
from typing import List

connected_clients: List[WebSocket] = []

async def add_client(websocket: WebSocket):
    connected_clients.append(websocket)

async def remove_client(websocket: WebSocket):
    """
    Remove a WebSocket connection from the list of connected clients.
    """
    if websocket in connected_clients:  # Check if it exists before removing
        connected_clients.remove(websocket)
        print(f"❌ WebSocket removed: {websocket.client}")
    else:
        print(f"⚠️ Tried to remove non-existent WebSocket: {websocket.client}")