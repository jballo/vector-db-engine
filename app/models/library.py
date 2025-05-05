from uuid import UUID
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class LibraryBase(BaseModel):
    name: str = Field(..., description="Legible library name")
    metadata: Dict[str, Any] = Field (
        default_factory=dict, description="Arbitrary key/value metadata"
    )

class LibraryCreate(LibraryBase):
    """Fields to create a new Library"""
    pass

class LibraryUpdate(BaseModel):
    """Fields that can be updated on an existing Library. Optional to allow partial updates."""
    name: Optional[str] = Field(None, description="New library name")
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Replacement metadata dict"
    )

class Library(LibraryBase):
    """Returned in read operations, include the generated ID"""
    id: UUID = Field(..., description="Unique library identifier")

    # allow Pydantic to do translation of ORM object (tbd)
    class Config:
        orm_mode = True

