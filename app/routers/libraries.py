from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_key_header
from .chunks import router as chunks_router
from .search import router as search_router

router = APIRouter(
    prefix="/libraries",
    tags=["libraries"],
    dependencies=[Depends(get_key_header)],
    responses={404: {"description": "Not found"}},
)

router.include_router(chunks_router)

router.include_router(search_router)

dummy_data = [
    {"id": 1, "name": "Info A", "content": "context X"},
    {"id": 2, "name": "Info B", "content": "context Y"},
    {"id": 3, "name": "Info C", "content": "context Z"},
]

@router.post("")
async def create_librarie():
    return {""}

@router.get("")
async def list_libraries():
    return dummy_data

@router.get("/{library_id}")
async def get_library(library_id: int):
    return {""}

@router.put("/{library_id}")
async def update_library(library_id: int):
    return {""}

@router.delete("/{library_id}")
async def delete_library(library_id: int):
    return {""}








