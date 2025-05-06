from uuid import UUID
from typing import List, Literal, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator, ValidationError, conlist, constr
from .chunk import Chunk
from .library import Library

class SearchRequest(BaseModel):
    """Paylod for a kNN search"""
    text: constr(min_length=1) = Field( # type: ignore
        ..., description="Query text to embed and search"
    )
    k: int = Field(
        ...,
        gt=0,
        description="Number of nearest neighbors to return (must be > 0)",
    )
    metric: Literal["cosine", "l2"] = Field(
        "cosine",
        description="Distance metric to use",
    )
    algorithm: Literal["brute", "vptree"] = Field(
        "brute", description="Search algorithm to use"
    )


class SearchResult(BaseModel):
    """One hit from a search"""
    chunk: Chunk = Field(..., description="Matched chunk")
    score: float = Field(
        ...,
        description="Similarity score (cosine) or distance (L2). Higher=more simiar for cosine; lower=closer for L2"
    )

class SearchHit(BaseModel):
    """
    - id: UUID of the chunk
    - score: similarity/distance
    """
    id: UUID = Field(..., description="Chunk ID")
    score: float = Field(..., description="Hit score")
