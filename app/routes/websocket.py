import asyncio
from redis import Redis
from fastapi import WebSocket, WebSocketDisconnect
from app.services import connected_clients

redis = Redis(host="localhost", port=6379, decode_responses=True)


async def broadcast_updates():
    """Broadcast updates to all connected clients"""
    pubsub = redis.pubsub()
    pubsub.subscribe("notes_channel")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            content = message["data"]
            for client in connected_clients:
                await client.send_json({ "type": "update", "content": content })
        await asyncio.sleep(0.1)

async def websocket_endpoint(websocket: WebSocket):
    """Handles websocket connections"""
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"New WebSocket connected. Total clients: {len(connected_clients)}")
    try:
        while True:
            data = await websocket.receive_json()
            print(f"data..., {data}")
            if data["type"] == "update":
                redis.publish("notes_channel", data["content"])
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print(f"WebSocket disconnected. Total clients: {len(connected_clients)}")