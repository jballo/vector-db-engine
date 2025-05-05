from fastapi import APIRouter, Depends, HTTPException
from .chunks import router as chunks_router

router = APIRouter(
    prefix="/{library_id}/documents",
    tags=["chunks"],
)

router.include_router(chunks_router)


@router.post("")
async def create_document(library_id: int):
    return {""}

@router.get("")
async def list_documents(library_id: int):
    return {""}

@router.get("/{document_id}")
async def get_document(library_id: int, document_id: int):
    return {""}

@router.put("/{document_id}")
async def update_document(library_id: int, document_id: int):
    return {""}

@router.delete("/{document_id}")
async def delete_document(library_id: int, document_id: int):
    return {""}

@router.post("/{document_id}/search")
async def search_document(library_id: int, document_id: int):
    return {""}