"""
In-memory database for development and testing.
This will be replaced with SQLAlchemy + MySQL in production.
"""

from datetime import datetime
from typing import Dict
from ..schemas.note import NoteInDB


# In-memory storage (will be replaced with actual database)
notes_db: Dict[int, dict] = {}
_id_counter: int = 0


def get_next_id() -> int:
    """Generate the next unique ID."""
    global _id_counter
    _id_counter += 1
    return _id_counter


def reset_db() -> None:
    """Reset the database (useful for testing)."""
    global notes_db, _id_counter
    notes_db = {}
    _id_counter = 0


# Seed with sample data
def seed_database() -> None:
    """Seed the database with sample notes for demonstration."""
    sample_notes = [
        {
            "title": "Introduction to Python",
            "content": "Python is a versatile programming language known for its simplicity and readability. Key concepts include variables, data types, and control structures.",
            "subject": "Computer Science",
            "student_name": "John Doe",
            "tags": ["python", "programming", "basics"]
        },
        {
            "title": "Calculus: Derivatives",
            "content": "The derivative represents the rate of change of a function. Key rules include power rule, product rule, and chain rule.",
            "subject": "Mathematics",
            "student_name": "Jane Smith",
            "tags": ["calculus", "derivatives", "math"]
        },
        {
            "title": "World War II Overview",
            "content": "World War II (1939-1945) was a global conflict involving most of the world's nations. Key events include D-Day, Pearl Harbor, and the atomic bombings.",
            "subject": "History",
            "student_name": "John Doe",
            "tags": ["history", "wwii", "war"]
        }
    ]
    
    for note_data in sample_notes:
        note_id = get_next_id()
        now = datetime.utcnow()
        notes_db[note_id] = {
            "id": note_id,
            **note_data,
            "created_at": now,
            "updated_at": now
        }


# Auto-seed on import for demo purposes
seed_database()
