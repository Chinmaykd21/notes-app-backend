import os
from fastapi import FastAPI
from app.graphql import schema
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routes import rest_router

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN", "http://localhost:5173")

app = FastAPI() # Initialize FastAPI app

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

"""
This file is important because we want to set /graphql as the 
endpoint for all GraphQL queries and mutations.
"""
grapql_app = GraphQLRouter(schema)
app.include_router(grapql_app, prefix="/graphql") # Add GraphQL endpoint at /graphql