import redis
import os
import json
import uuid
from dotenv import load_dotenv

# ✅ Load .env variables
load_dotenv()

class RedisStore:
    """
    Handles storing notes in Redis instead of in-memory.
    """
    def __init__(self):
        REDIS_URL = os.getenv("REDIS_URL")
        self.redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

    def add_note(self, content: str) -> str:
        """
        Adds a new note to Redis and returns its ID.
        """
        note_id = str(uuid.uuid4())  # Generate unique ID
        self.redis_client.set(note_id, json.dumps({"id": note_id, "content": content}))
        return note_id

    def get_notes(self):
        """
        Retrieves all notes stored in Redis.
        """
        keys = self.redis_client.keys()
        notes = []
        for k in keys:
            note = self.redis_client.get(k)
            if note:
                notes.append(json.loads(note))  # ✅ Properly parse JSON
        return notes

    def get_note(self, note_id: str):
        """
        Retrieves a single note by ID.
        """
        note = self.redis_client.get(note_id)
        if note:
            parsed_note = json.loads(note)  # ✅ Parse JSON string
            return {"id": parsed_note["id"], "content": parsed_note["content"]}  # ✅ Ensure correct structure
        return None

    def update_note(self, note_id: str, content: str):
        """
        Updates an existing note.
        """
        if self.redis_client.exists(note_id):
            self.redis_client.set(note_id, json.dumps({"id": note_id, "content": content}))
            return True
        return False

    def delete_note(self, note_id: str):
        """
        Deletes a note by ID.
        """
        return self.redis_client.delete(note_id) > 0

# ✅ Create a single Redis store instance
redis_store = RedisStore()
