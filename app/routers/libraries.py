from fastapi import APIRouter, Depends, HTTPException, Body, Path, status
from typing import List
from uuid import uuid4, UUID

from ..dependencies import get_key_header
# from .chunks import router as chunks_router
from .documents import router as documents_router
from ..models.library import Library, LibraryCreate, LibraryUpdate
from ..models.search import SearchRequest, SearchResult


router = APIRouter(
    prefix="/libraries",
    tags=["libraries"],
    dependencies=[Depends(get_key_header)],
    responses={404: {"description": "Not found"}},
)

router.include_router(documents_router)


# simple in-memory store
_fake_db: List[Library] = []

@router.post(
    "",
    response_model=Library,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Library",
)
async def create_library(
    payload: LibraryCreate = Body(
        ..., description="Name + metadata for the new library"
    ),
) -> Library:  
    lib = Library(id=uuid4(), **payload.model_dump())
    _fake_db.append(lib)
    return lib


@router.get(
    "",
    response_model=List[Library],
    status_code=status.HTTP_200_OK,
    summary="List all Libraries",
)
async def list_libraries() -> List[Library]:
    return _fake_db


@router.get(
    "/{library_id}",
    response_model=Library,
    status_code=status.HTTP_200_OK,
    summary="Get a Library by ID",
)
async def get_library(library_id: UUID = Path(..., description="UUID of the library")) -> Library:
    for lib in _fake_db:
        if lib.id == library_id:
            return lib
    raise HTTPException(status_code=404, detail="Library not found")


@router.put(
    "/{library_id}",
    response_model=Library,
    status_code=status.HTTP_200_OK,
    summary="Update an existing Library",
)
async def update_library(
    library_id: UUID = Path(..., description="UUID of the library"),
    payload: LibraryUpdate = Body(
        ..., description="Fields to update (all optional)"
    ),
) -> Library:
    for idx, lib in enumerate(_fake_db):
        if lib.id == library_id:
            updated = lib.model_copy(update=payload.model_dump(exclude_none=True))
            _fake_db[idx] = updated
            return updated
    
    raise HTTPException(status_code=404, detail="Library not found")

@router.delete(
    "/{library_id}",
    response_model=Library,
    status_code=status.HTTP_200_OK,
    summary="Delete a Library",
)
async def delete_library(library_id: UUID = Path(..., description="UUID of the library")) -> Library:
    for idx, lib in enumerate(_fake_db):
        if lib.id == library_id:
            return _fake_db.pop(idx)
    
    raise HTTPException(status_code=404, detail="Library not found")

@router.post(
    "/{library_id}/search",
    response_model=List[SearchResult],
    status_code=status.HTTP_200_OK,
    summary="kNN search within a Library",
)
async def search_library(
    library_id: UUID = Path(..., description="UUID of the library"),
    payload: SearchRequest = Body(..., description="Search parameters"),
) -> List[SearchResult]:
    return []









