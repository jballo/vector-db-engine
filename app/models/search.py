from uuid import UUID
from typing import List, Literal, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator, ValidationError, conlist
from .chunk import Chunk

class SearchRequest(BaseModel):
    """Paylod for a kNN search"""
    query_embedding: conlist(
        float, min_length=1 # type: ignore
    ) = Field(..., description="Embedding vector search with (Non-empty list of floats)")
    k: int = Field(
        ...,
        gt=0,
        description="Number of nearest neighbors to return (must be > 0)",
    )
    metric: Literal["cosine", "l2"] = Field(
        "cosine",
        description="Distance metric to use",
    )
    filter: Optional[Dict[str, Any]] = Field(
        None,
        description=("Optional metadata filter: only consider chunks whose metadata dict contains these key/value pairs")
    )

    @model_validator(mode="after")
    def ensure_filter_keys_are_str(cls, model):
        """Runs after fields are parsed. Enforces that all filter-keys are str"""
        if model.filter is not None:
            bad = [k for k in model.filter if not isinstance(k, str)]
            if bad:
                raise ValidationError(
                    [
                        {
                            "loc": ("filter",),
                            "msg": f"filter keys must be strings, "
                                   f"got {bad!r}",
                            "type": "value_error",
                        }
                    ],
                    model=cls,
                )
        
        return model

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
