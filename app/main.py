import os
from fastapi import FastAPI, Request, Response
from app.graphql import schema
from app.routes import rest_router
from strawberry.asgi import GraphQL
from fastapi.middleware.cors import CORSMiddleware

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN", "http://localhost:5173")

app = FastAPI() # Initialize FastAPI app
print("FRONTEND_DOMAIN:", os.getenv("FRONTEND_DOMAIN"))

# Add CORS middleware to allow only frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_DOMAIN],
    allow_credentials=True, # Allow cookies and authentication
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Limit allowed methods
    allow_headers=["Authorization", "Content-Type"],  # Limit allowed headers
)

# Secure Explicit Pre-flight handling
@app.options("/{full_path:path}")
async def preflight_handler(full_path:str, request: Request):
    origin = request.headers.get("Origin")
    if origin != FRONTEND_DOMAIN:
        return Response(status_code=403) # Reject unauthorized request
    
    return Response(headers={
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type"
    })

# REST endpoints
app.include_router(rest_router)

# GraphQL route
app.add_route("/graphql", GraphQL(schema))