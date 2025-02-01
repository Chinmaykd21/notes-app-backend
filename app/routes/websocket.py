import json
from fastapi import WebSocket
from typing import List
class WebSocketManager:
    """
        Manages active WebSocket connection.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
            Accepts a WebSocket connection and adds to the list of active connections
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
            Removes a WebSocket connection when it closes.
        """
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """
            Sends a message to all connected clients.
        """
        message_str = json.dumps(message) # ✅ Convert back to JSON before sending
        print("📤 Broadcasting WebSocket message:", message_str)

        for connection in self.active_connections:
            await connection.send_text(message_str)  # ✅ Use send_text() (NOT send())

# A single instance to manage all websocket connections.
websocket_manager = WebSocketManager()