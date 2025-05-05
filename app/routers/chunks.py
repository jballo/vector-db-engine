from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/{library_id}/chunks",
    tags=["chunks"],
)


@router.post("")
async def create_chunk(library_id: int):
    return {""}

@router.get("")
async def list_chunks(library_id: int):
    return {""}

@router.get("/{chunk_id}")
async def get_chunk(library_id: int, chunk_id: int):
    return {""}

@router.put("/{chunk_id}")
async def update_chunk(library_id: int, chunk_id: int):
    return {""}

@router.delete("/{chunk_id}")
async def delete_chunk(library_id: int, chunk_id: int):
    return {""}