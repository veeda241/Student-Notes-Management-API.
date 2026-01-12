"""
Database seeder to populate default values.
"""

from sqlalchemy.orm import Session
from ..models.note import Note

def seed_database(db: Session):
    """
    Seed the database with sample notes if it is empty.
    """
    # Check if data exists
    if db.query(Note).first():
        return

    sample_notes = [
        Note(
            title="Introduction to Python",
            content="Python is a versatile programming language known for its simplicity and readability. Key concepts include variables, data types, and control structures.",
            subject="Computer Science",
            student_name="John Doe",
            tags=["python", "programming", "basics"]
        ),
        Note(
            title="Calculus: Derivatives",
            content="The derivative represents the rate of change of a function. Key rules include power rule, product rule, and chain rule.",
            subject="Mathematics",
            student_name="Jane Smith",
            tags=["calculus", "derivatives", "math"]
        ),
        Note(
            title="World War II Overview",
            content="World War II (1939-1945) was a global conflict involving most of the world's nations. Key events include D-Day, Pearl Harbor, and the atomic bombings.",
            subject="History",
            student_name="John Doe",
            tags=["history", "wwii", "war"]
        ),
        Note(
            title="FastAPI basics",
            content="FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints.",
            subject="Computer Science",
            student_name="Alice Johnson",
            tags=["fastapi", "api", "python"]
        ),
        Note(
            title="Organic Chemistry: Alkanes",
            content="Alkanes are acyclic saturated hydrocarbons. They consist of hydrogen and carbon atoms arranged in a tree structure in which all the carbon–carbon bonds are single.",
            subject="Chemistry",
            student_name="Bob Wilson",
            tags=["science", "chemistry", "organic"]
        )
    ]

    db.add_all(sample_notes)
    db.commit()
    print("🌱 Database seeded with default notes!")
