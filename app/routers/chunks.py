from fastapi import APIRouter, Depends, HTTPException, Path, status, Body
from typing import List
from uuid import uuid4, UUID
from ..models.chunk import Chunk, ChunkCreate, ChunkUpdate

router = APIRouter(
    prefix="/{document_id}/chunks",
    tags=["chunks"],
)

# simple in-memory store
_fake_db: List[Chunk] = []

@router.post(
    "",
    response_model=Chunk,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Chunk"
)
async def create_chunk(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
    payload: ChunkCreate = Body(..., description="text + embedding + metadata"),
) -> Chunk:
        chunk = Chunk(id=uuid4(), document_id=document_id, library_id=library_id, **payload.model_dump())
        _fake_db.append(chunk)
        return chunk;

@router.get(
    "",
    response_model=List[Chunk],
    status_code=status.HTTP_200_OK,
    summary="List all chunks in respective library + id"
)
async def list_chunks(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
) -> List[Chunk]:
    chunks = [chunk for chunk in _fake_db if (chunk.library_id == library_id and chunk.document_id == document_id)]
    return chunks

@router.get(
    "/{chunk_id}",
    response_model=Chunk,
    status_code=status.HTTP_200_OK,
    summary="Get a chunk with library id, document id, and chunk id",
)
async def get_chunk(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
    chunk_id: UUID = Path(..., description="UUID of the chunk"),
) -> Chunk:
    for chunk in _fake_db:
        if chunk.library_id == library_id and chunk.document_id == document_id and chunk.id == chunk_id:
             return chunk
        
    raise HTTPException(status_code=404, detail="Chunk not found")

@router.put(
    "/{chunk_id}",
    response_model=Chunk,
    status_code=status.HTTP_200_OK,
    summary="Update an existing chunk",
)
async def update_chunk(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
    chunk_id: UUID = Path(..., description="UUID of the chunk"),
    payload: ChunkUpdate = Body(..., description="Field to update (all optional)"),
) -> Chunk:
    for idx, chunk in enumerate(_fake_db):
         if chunk.library_id == library_id and chunk.document_id == document_id and chunk.id == chunk_id:
              updated = chunk.model_copy(update=payload.model_dump(exclude_none=True))
              _fake_db[idx] = updated
              return updated
         
    raise HTTPException(status_code=404, detail="Chunk not found")

@router.delete(
    "/{chunk_id}",
    response_model=Chunk,
    status_code=status.HTTP_200_OK,
    summary="Delete a chunk",
)
async def delete_chunk(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
    chunk_id: UUID = Path(..., description="UUID of the chunk"),
) -> Chunk:
    for idx, chunk in enumerate(_fake_db):
         if chunk.library_id == library_id and chunk.document_id == document_id and chunk.id == chunk_id:
              return _fake_db.pop(idx)
         
    raise HTTPException(status_code=404, detail="Chunk not found")