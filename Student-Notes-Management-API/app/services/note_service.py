"""
Note service containing business logic for CRUD operations.
Separates business logic from route handlers for better testability.
"""

from datetime import datetime
from typing import List, Optional, Tuple, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc, String

from ..models.note import Note
from ..schemas.note import NoteCreate, NoteUpdate, NoteInDB


class NoteService:
    """Service class for note-related operations using SQLAlchemy."""
    
    @staticmethod
    def get_all_notes(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        subject: Optional[str] = None,
        student_name: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Note], int]:
        """
        Get all notes with optional filtering and pagination.
        """
        query = db.query(Note)
        
        # Apply filters
        if subject:
            query = query.filter(func.lower(Note.subject) == subject.lower())
        
        if student_name:
            query = query.filter(func.lower(Note.student_name) == student_name.lower())
        
        if search:
            search_param = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Note.title).like(search_param),
                    func.lower(Note.content).like(search_param)
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting (newest first) and pagination
        notes = query.order_by(desc(Note.updated_at))\
                     .offset((page - 1) * page_size)\
                     .limit(page_size)\
                     .all()
        
        return notes, total
    
    @staticmethod
    def get_note_by_id(db: Session, note_id: int) -> Optional[Note]:
        """Get a single note by ID."""
        return db.query(Note).filter(Note.id == note_id).first()
    
    @staticmethod
    def create_note(db: Session, note_data: NoteCreate) -> Note:
        """Create a new note."""
        new_note = Note(
            title=note_data.title,
            content=note_data.content,
            subject=note_data.subject,
            student_name=note_data.student_name,
            tags=note_data.tags
        )
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return new_note
    
    @staticmethod
    def update_note(db: Session, note_id: int, note_data: NoteUpdate) -> Optional[Note]:
        """Update an existing note."""
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return None
        
        update_data = note_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(note, key, value)
            
        db.commit()
        db.refresh(note)
        return note
    
    @staticmethod
    def delete_note(db: Session, note_id: int) -> bool:
        """Delete a note by ID."""
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return False
            
        db.delete(note)
        db.commit()
        return True
    
    @staticmethod
    def get_all_subjects(db: Session) -> List[str]:
        """Get all unique subjects."""
        # Query distinct subjects
        results = db.query(Note.subject).distinct().all()
        return sorted([r[0] for r in results])
    
    @staticmethod
    def get_all_students(db: Session) -> List[str]:
        """Get all unique student names."""
        results = db.query(Note.student_name).distinct().all()
        return sorted([r[0] for r in results])
    
    @staticmethod
    def get_notes_by_tag(db: Session, tag: str) -> List[Note]:
        """
        Get all notes with a specific tag.
        
        Note: Since tags are stored as JSON list, searching depends on the DB backend.
        For simple SQLite/relational compatibility, we might need to fetch and filter,
        or use specific JSON operators if available.
        For simplicity and compatibility: fetching relevant or all records (if small) 
        is safer across generic SQL, but inefficient. 
        For this demo, we'll implement a Python-side filter on fetched data 
        or use a LIKE query if tags are stored stringified (they are JSON array).
        
        Using a simple LIKE on the TEXT representation of the JSON column is a hacky 
        but effective DB-agnostic way for this simple 'tag' search.
        """
        search_param = f"%{tag}%"
        # This assumes tags are stored as text/JSON string in DB
        # While not perfect, it works for basic searching in simple schema
        notes = db.query(Note).filter(func.cast(Note.tags, String).like(search_param)).all()
        
        # Double check in python to be sure (avoid partial matches like "ban" matching "banana")
        return [n for n in notes if tag in n.tags]
