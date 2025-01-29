from fastapi import APIRouter
from app.services import connected_clients

router = APIRouter()

@router.get("/")
def read_root():
    return { "message": "Welcome to real-time notes app" }

@router.get("/health")
def health_check():
    return { "status": "ok" }

@router.get("/clients")
def get_connected_clients():
    print(f"📢 Total Connected Clients: {len(connected_clients)}")  # Debug log
    return { "connected_clients": len(connected_clients) }