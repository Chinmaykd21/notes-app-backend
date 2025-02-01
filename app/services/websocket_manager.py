import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.routes import websocket_manager

websocket_router = APIRouter()

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
        Websocket endpoint for real-time updates
    """
    await websocket_manager.connect(websocket)
    print("websocket connected")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"websocket data received - {data}")
            try:
                message = json.loads(data)  # ✅ Convert raw text to a dictionary
            except json.JSONDecodeError:
                print("❌ Invalid JSON format received:", data)
                continue  # Skip processing invalid data

            if not isinstance(message, dict):  # ✅ Ensure it's a dictionary
                print("❌ Unexpected message format:", message)
                continue

            if message.get("type") in ["note_create", "note_update", "note_delete"]:
                await websocket_manager.broadcast(message)  
    except WebSocketDisconnect:
        print("❌ WebSocket disconnected")
        websocket_manager.disconnect(websocket)