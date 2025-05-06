from fastapi import APIRouter, Depends, HTTPException, Body, Path, status
from typing import List
from uuid import uuid4, UUID

from ..dependencies import get_key_header
# from .chunks import router as chunks_router
from .documents import router as documents_router
from ..models.library import Library, LibraryCreate, LibraryUpdate
from ..models.search import SearchRequest, SearchResult

from ..service.library_service import create_library_service, list_libraries_service, get_library_service, update_library_service, delete_library_service

from ..service.search_service import search_library_service
from ..config import Config

import cohere

CO_API_KEY = Config.COHERE_KEY
co = cohere.ClientV2(api_key=CO_API_KEY)


router = APIRouter(
    prefix="/libraries",
    tags=["libraries"],
    dependencies=[Depends(get_key_header)],
    responses={404: {"description": "Not found"}},
)

router.include_router(documents_router)

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
    return create_library_service(payload)


@router.get(
    "",
    response_model=List[Library],
    status_code=status.HTTP_200_OK,
    summary="List all Libraries",
)
async def list_libraries() -> List[Library]:
    return list_libraries_service()


@router.get(
    "/{library_id}",
    response_model=Library,
    status_code=status.HTTP_200_OK,
    summary="Get a Library by ID",
)
async def get_library(library_id: UUID = Path(..., description="UUID of the library")) -> Library:
    try:
        return get_library_service(library_id)
    except KeyError:
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
    try:
        return update_library_service(library_id, payload)
    except KeyError:
        raise HTTPException(status_code=404, detail="Library not found")

@router.delete(
    "/{library_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Library",
)
async def delete_library(library_id: UUID = Path(..., description="UUID of the library")) -> None:
    try:
        delete_library_service(library_id)
    except KeyError:
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
    """top-k most similar chunks within the given library"""
    try:
        text = payload.text
        response = co.embed(
            texts=[text],
            model="embed-v4.0",
            input_type="classification",
            embedding_types=["float"]
        )
        embedding = response.embeddings.float_[0]
        payload.query_embedding = embedding

        return search_library_service(
            library_id=library_id,
            query_embedding=payload.query_embedding,
            k=payload.k,
            metric=payload.metric,
            metadata_filter=payload.filter,
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library {library_id} not found",
        )









