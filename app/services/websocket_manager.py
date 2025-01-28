from fastapi import WebSocket
from typing import List

connected_clients: List[WebSocket] = []

async def add_client(websocket: WebSocket):
    connected_clients.append(websocket)

async def remove_client(websocket: WebSocket):
    connected_clients.remove(websocket)

async def broadcast(content: str):
    for client in connected_clients:
        await client.send_json({ "type": "update", "content": content })