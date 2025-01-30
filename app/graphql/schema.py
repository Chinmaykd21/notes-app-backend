import strawberry
from typing import List, Optional
from app.services import memory_store

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
        Retrieves all notes from memory.
        """
        return [Note(**note) for note in memory_store.get_notes()]

    @strawberry.field
    def note_by_id(self, note_id: str) -> Optional[Note]:
        """
        Retrieves a note by its ID.
        """
        note_content = memory_store.get_note(note_id)
        if note_content:
            return Note(id=note_id, content=note_content)
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_note(self, content: str) -> Note:
        """
        Adds a new note and returns the created note.
        """
        note_id = memory_store.add_note(content)
        return Note(id=note_id, content=content)

    @strawberry.mutation
    def update_note(self, note_id: str, content: str) -> bool:
        """
        Updates an existing note.
        """
        return memory_store.update_note(note_id, content)

    @strawberry.mutation
    def delete_note(self, note_id: str) -> bool:
        """
        Deletes a note by ID.
        """
        return memory_store.delete_note(note_id)

# ✅ Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
