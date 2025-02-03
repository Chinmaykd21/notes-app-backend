import json
from fastapi import WebSocket
from typing import List, Dict
class WebSocketManager:
    """
        Manages active WebSocket connection.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connected_users: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        """
            Accepts a WebSocket connection and adds to the list of active connections
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connected_users[websocket] = username
        # Broadcast the user joined
        import asyncio
        asyncio.create_task(self.broadcast({ "type": "user_joined", "user": username }))

    def disconnect(self, websocket: WebSocket):
        """
            Removes a WebSocket connection when it closes.
        """
        if websocket in self.active_connections:
            username = self.connected_users.get(websocket, "Unknown uesr")
            self.active_connections.remove(websocket)
            del self.connected_users[websocket]

            # Broadcast that user has left
            import asyncio
            asyncio.create_task(self.broadcast({ "type": "user_left", "user": username }))
        return None

    async def broadcast(self, message: dict):
        """
            Sends a message to all connected clients.
        """
        message_str = json.dumps(message) # ✅ Convert back to JSON before sending

        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception:
                print(f"❌ Failed to send message to {connection}")

# A single instance to manage all websocket connections.
websocket_manager = WebSocketManager()