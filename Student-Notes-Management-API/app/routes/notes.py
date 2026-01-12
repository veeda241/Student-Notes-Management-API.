"""
Notes API routes with full CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import List, Optional
from sqlalchemy.orm import Session

from ..schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NoteListResponse,
    MessageResponse
)
from ..services import NoteService
from ..database import get_db

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get(
    "/",
    response_model=NoteListResponse,
    summary="Get all notes",
    description="Retrieve a paginated list of notes with optional filtering."
)
async def get_notes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    student_name: Optional[str] = Query(None, description="Filter by student name"),
    search: Optional[str] = Query(None, description="Search in title and content"),
    db: Session = Depends(get_db)
):
    """Get all notes with pagination and filtering."""
    notes, total = NoteService.get_all_notes(
        db=db,
        page=page,
        page_size=page_size,
        subject=subject,
        student_name=student_name,
        search=search
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return NoteListResponse(
        notes=notes,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get(
    "/subjects",
    response_model=List[str],
    summary="Get all subjects",
    description="Retrieve a list of all unique subjects."
)
async def get_subjects(db: Session = Depends(get_db)):
    """Get all unique subjects in the system."""
    return NoteService.get_all_subjects(db)


@router.get(
    "/students",
    response_model=List[str],
    summary="Get all students",
    description="Retrieve a list of all unique student names."
)
async def get_students(db: Session = Depends(get_db)):
    """Get all unique student names in the system."""
    return NoteService.get_all_students(db)


@router.get(
    "/tag/{tag}",
    response_model=List[NoteResponse],
    summary="Get notes by tag",
    description="Retrieve all notes with a specific tag."
)
async def get_notes_by_tag(tag: str, db: Session = Depends(get_db)):
    """Get all notes that have a specific tag."""
    return NoteService.get_notes_by_tag(db, tag)


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Get a note by ID",
    description="Retrieve a single note by its unique identifier."
)
async def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a specific note by ID."""
    note = NoteService.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )
    return note


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create a new note with the provided data."
)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note."""
    return NoteService.create_note(db, note)


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Update a note",
    description="Update an existing note with partial data."
)
async def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    """Update an existing note."""
    updated_note = NoteService.update_note(db, note_id, note)
    if not updated_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )
    return updated_note


@router.delete(
    "/{note_id}",
    response_model=MessageResponse,
    summary="Delete a note",
    description="Delete a note by its unique identifier."
)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note by ID."""
    if not NoteService.delete_note(db, note_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {note_id} not found"
        )
    return MessageResponse(
        message=f"Note with ID {note_id} has been deleted successfully",
        success=True
    )
