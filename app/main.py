import os
import uvicorn
from fastapi import FastAPI
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# REST endpoints
app.include_router(rest_router)

# GraphQL route
app.add_route("/graphql", GraphQL(schema))