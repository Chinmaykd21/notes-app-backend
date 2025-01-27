from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.routes.rest import router as rest_router

app = FastAPI() # Initialize FastAPI app

# REST endpoints
app.include_router(rest_router)

# GraphQL endpoints
import strawberry

@strawberry.type
class Note:
    id: int
    content: str

notes = [] # In-memory storage for notes

"""
Resolvers for Notes: Provides a structure for adding and fetching notes, 
which can be extended later with a database.
"""
@strawberry.type
class Query:
    # Resolver for fetchng all notes
    @strawberry.field
    def get_notes(self) -> list[Note]:
        return notes

@strawberry.type
class Mutation:
    # Resolver for adding a new note
    @strawberry.mutation
    def add_note(self, content:str) -> Note:
        note = Note(id=len(notes) + 1, content=content)
        notes.append(note)
        return note

# Define graphql schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
grapql_app = GraphQLRouter(schema)

"""
This file is important because we want to set /graphql as the 
endpoint for all GraphQL queries and mutations.
"""
app.include_router(grapql_app, prefix="/graphql") # Add GraphQL endpoint at /graphql