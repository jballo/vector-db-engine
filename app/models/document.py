from uuid import UUID
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Document metadata"
    )
    chunk_ids: List[UUID] = Field(
        default_factory=list, description="Ordered list of chunk IDs"
    )


class DocumentCreate(DocumentBase):
    """Fields required to create a new Document"""
    pass


class DocumentUpdate(BaseModel):
    metadata: Optional[Dict[str, Any]] = None
    chunk_ids: Optional[List[UUID]] = None


class Document(DocumentBase):
    id: UUID = Field(..., description="Unique document identifier")
    library_id: UUID = Field(..., description="Owning library ID")

    class Config:
        orm_mode = True
