from fastapi import APIRouter, Depends, HTTPException, Path, status, Body
from typing import List
from uuid import uuid4, UUID
from ..models.chunk import Chunk, ChunkCreate, ChunkUpdate
from ..service.chunk_service import create_chunk_service, list_chunks_service, get_chunk_service, update_chunk_service, delete_chunk_service

router = APIRouter(
    prefix="/{document_id}/chunks",
    tags=["chunks"],
)

# simple in-memory store
# _fake_db: List[Chunk] = []

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
        try:
             return create_chunk_service(library_id, document_id, payload)
        except KeyError:
             raise HTTPException("Parent library or document not found")

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
    try:
        return list_chunks_service(library_id, document_id)
    except KeyError:
        raise HTTPException("Parent library or document not found")


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
    try:
         return get_chunk_service(library_id, document_id, chunk_id)
    except KeyError:
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
    try:
         return update_chunk_service(library_id, document_id, chunk_id, payload)
    except KeyError:
        raise HTTPException(status_code=404, detail="Chunk not found")

@router.delete(
    "/{chunk_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a chunk",
)
async def delete_chunk(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
    chunk_id: UUID = Path(..., description="UUID of the chunk"),
) -> None:
    try:
        delete_chunk_service(library_id, document_id, chunk_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Chunk not found")