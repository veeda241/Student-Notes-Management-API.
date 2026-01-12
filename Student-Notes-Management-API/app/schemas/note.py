"""
Pydantic schemas for Note data validation.
Provides clear separation between input, output, and database models.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class NoteBase(BaseModel):
    """Base schema with common note attributes."""
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the note",
        examples=["Introduction to Python"]
    )
    content: str = Field(
        ...,
        min_length=1,
        description="Full content of the note",
        examples=["Python is a versatile programming language..."]
    )
    subject: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Academic subject of the note",
        examples=["Computer Science"]
    )
    student_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the student",
        examples=["John Doe"]
    )
    tags: List[str] = Field(
        default_factory=list,
        description="List of tags for categorization",
        examples=[["python", "programming", "basics"]]
    )


class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating an existing note. All fields are optional."""
    
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated title"
    )
    content: Optional[str] = Field(
        None,
        min_length=1,
        description="Updated content"
    )
    subject: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated subject"
    )
    student_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Updated student name"
    )
    tags: Optional[List[str]] = Field(
        None,
        description="Updated tags list"
    )


class NoteResponse(NoteBase):
    """Schema for note responses with all fields."""
    
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class NoteInDB(NoteResponse):
    """Schema representing a note as stored in the database."""
    pass


class NoteListResponse(BaseModel):
    """Schema for paginated list of notes."""
    
    notes: List[NoteResponse] = Field(..., description="List of notes")
    total: int = Field(..., description="Total number of notes")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")


class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")
