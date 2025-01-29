import json
import asyncio
from asyncio import Queue
from app.services import redis
from fastapi import WebSocket, WebSocketDisconnect
from app.services import connected_clients, batch_publish, remove_client, subscribe_to_note_channel

async def broadcast_updates():
    """
    Broadcast updates from Redis Pub/Sub to all connected WebSocket clients.
    """
    pubsub = await subscribe_to_note_channel(redis, "notes_channel")
    print("✅ Subscribed to Redis channel 'notes_channel'")  # ✅ Debugging log

    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
        
        if message and message["type"] == "message":
            raw_content = message["data"]
            
            # ✅ FIX: Decode bytes and parse JSON
            try:
                content_str = raw_content.decode("utf-8")  # Decode bytes to string
                content = json.loads(content_str)  # Parse string as JSON
                print(f"📩 Redis PubSub received: {content}")  # ✅ Debugging log

                # Send to all connected WebSockets
                for client in connected_clients:
                    try:
                        print(f"📢 Sending to client {client.client}")  # ✅ Debugging log
                        await client.send_json({"type": "update", "content": content})
                    except Exception as e:
                        print(f"⚠️ Error sending WebSocket message: {e}")
            
            except Exception as e:
                print(f"❌ Error decoding Redis message: {e} | Raw Data: {raw_content}")

        await asyncio.sleep(0.1)  # ✅ Prevents high CPU usage

async def websocket_endpoint(websocket: WebSocket):
    """
        Handles websocket connections with debouncing
    """
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"New WebSocket connected. Total clients: {len(connected_clients)}")

    update_queue = Queue()
    asyncio.create_task(batch_publish(redis, "notes_channel", update_queue))

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "update":
                delta = { "position": data["position"], "text": data["text"] } # Extract only the changed content
                await update_queue.put(delta) # Queue only the change and not the full content
    except WebSocketDisconnect:
        await remove_client(websocket)
        print(f"❌ WebSocket disconnected. Total clients: {len(connected_clients)}")
    except Exception as e:
        await remove_client(websocket)
        print(f"⚠️ WebSocket Error: {e}")