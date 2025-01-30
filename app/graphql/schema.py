import strawberry
from typing import List, Optional
from app.services import redis_store

@strawberry.type
class Note:
    """
    Defines the GraphQL Note type.
    """
    id: str
    content: str

@strawberry.type
class Query:
    @strawberry.field
    def notes(self) -> List[Note]:
        """
        Retrieves all notes stored in Redis.
        """
        return [Note(id=note["id"], content=note["content"]) for note in redis_store.get_notes()]

    @strawberry.field
    def note_by_id(self, note_id: str) -> Optional[Note]:
        """
        Retrieves a note by its ID.
        """
        note_data = redis_store.get_note(note_id)
        if note_data:
            # ✅ Ensure we’re returning a correctly formatted Note object
            return Note(id=note_data["id"], content=note_data["content"])
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_note(self, content: str) -> Note:
        """
        Adds a new note and returns it.
        """
        note_id = redis_store.add_note(content)
        return Note(id=note_id, content=content)

    @strawberry.mutation
    def update_note(self, note_id: str, content: str) -> bool:
        """
        Updates an existing note.
        """
        return redis_store.update_note(note_id, content)

    @strawberry.mutation
    def delete_note(self, note_id: str) -> bool:
        """
        Deletes a note by ID.
        """
        return redis_store.delete_note(note_id)

# ✅ Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
