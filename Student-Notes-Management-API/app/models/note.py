"""
SQLAlchemy Note model for database persistence.
Ready for MySQL integration.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Note(Base):
    """
    Note model representing a student's note in the database.
    
    Attributes:
        id: Unique identifier
        title: Note title
        content: Full note content
        subject: Academic subject
        student_name: Name of the student who created the note
        tags: List of tags for categorization
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    subject = Column(String(100), nullable=False, index=True)
    student_name = Column(String(100), nullable=False, index=True)
    tags = Column(JSON, default=list)  # Stored as JSON array
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Note(id={self.id}, title='{self.title}', subject='{self.subject}')>"
