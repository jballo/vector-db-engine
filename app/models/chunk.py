from uuid import UUID
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, conlist

# Note: conlist ensures non-empty list

class ChunkBase(BaseModel):
    text: str = Field(..., description="Raw text of this chunk")
    embedding: conlist(  # type: ignore
        float, min_length=1
    ) = Field(..., description="Embedding vector")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary chunk metadata"
    )

class ChunkCreate(ChunkBase):
    """Fields required to create a new Chunk"""
    pass

class ChunkUpdate(BaseModel):
    """
    Partial update for a Chunk; any field may be omitted.
    """
    text: Optional[str] = Field(None, description="Updated text")
    embedding: Optional[conlist(float, min_length=1)] = Field( # type: ignore
        None, description="Updated embedding"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Updated metadata"
    )

class Chunk(ChunkBase):
    """
    Returned from read operations; includes IDs.
    """
    id: UUID = Field(..., description="Unique chunk identifier")
    library_id: UUID = Field(..., description="Parent library ID")
    document_id: UUID = Field(
        None, description="Optional parent document ID"
    )

    class Config:
        orm_mode = True