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
    print('accepted')
    try:
        while True:
            data = await websocket.receive_text()
            print('got data')
            message = json.loads(data) # converts a JSON object to python dictionary when receiving
            if message.get("type") in ["note_create", "note_update", "note_delete"]:
                # json.dumps converts python dictionary to a JSON string before sending
                print(f"message - {message}")
                await websocket_manager.broadcast(json.dumps(message))  # ✅ Broadcast update
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)