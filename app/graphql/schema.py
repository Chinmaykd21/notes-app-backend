
# GraphQL endpoints
import strawberry
from .models import Note

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