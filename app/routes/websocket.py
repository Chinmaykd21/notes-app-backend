import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services import websocket_manager

websocket_router = APIRouter()

@websocket_router.websocket("/ws") # Accept username as a parameter
async def websocket_endpoint(websocket: WebSocket, username: str = Query("Guest")):
    """
        Websocket endpoint for real-time updates
    """
    await websocket_manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            print("data", data)
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