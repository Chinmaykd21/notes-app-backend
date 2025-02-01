import os
from fastapi import FastAPI, Request, Response
from app.graphql import schema
from app.routes import rest_router
from strawberry.asgi import GraphQL
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.services import websocket_router

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN", "http://localhost:5173")

app = FastAPI() # Initialize FastAPI app

# Secure Explicit Pre-flight handling
@app.options("/graphql")
async def preflight_handler(request: Request):
    origin = request.headers.get("Origin")
    if origin != FRONTEND_DOMAIN:
        print(f"❌ Unauthorized preflight request from: {origin}")
        return Response(status_code=403) # Reject unauthorized request
    
    print("✅ Handling GraphQL Preflight Request")
    return Response(headers={
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type",
        "Access-Control-Allow-Credentials": "true",
    })

# REST endpoints
app.include_router(rest_router)
# GraphQl endpoints
graphql_router = APIRouter()
graphql_router.add_route("/graphql", GraphQL(schema), methods=["GET", "POST", "PUT", "DELETE"])
graphql_router.add_route("/graphql", GraphQL(schema), methods=["OPTIONS"])
app.include_router(graphql_router)
# Websocket
app.include_router(websocket_router);


# Add CORS middleware to allow only frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_DOMAIN],
    allow_credentials=True, # Allow cookies and authentication
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Limit allowed methods
    allow_headers=["Authorization", "Content-Type"],  # Limit allowed headers
)