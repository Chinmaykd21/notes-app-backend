from typing import Dict
import uuid

class MemoryStore:
    """
    Simple in-memory store for notes.
    """
    def __init__(self):
        self.notes: Dict[str, str] = {}  # Stores notes as {id: content}

    def add_note(self, content: str) -> str:
        """
        Adds a new note to the store and returns its ID.
        """
        note_id = str(uuid.uuid4())  # Generate unique ID
        self.notes[note_id] = content
        return note_id

    def get_notes(self):
        """
        Retrieves all notes as a list of dictionaries.
        """
        return [{"id": note_id, "content": content} for note_id, content in self.notes.items()]

    def get_note(self, note_id: str):
        """
        Retrieves a single note by ID.
        """
        return self.notes.get(note_id, None)

    def update_note(self, note_id: str, content: str):
        """
        Updates an existing note. Returns True if updated, False if not found.
        """
        if note_id in self.notes:
            self.notes[note_id] = content
            return True
        return False

    def delete_note(self, note_id: str):
        """
        Deletes a note by ID. Returns True if deleted, False if not found.
        """
        return self.notes.pop(note_id, None) is not None

# ✅ Create a single instance of the memory store
memory_store = MemoryStore()
