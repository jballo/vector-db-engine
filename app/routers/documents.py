from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from typing import List
from uuid import uuid4, UUID
from .chunks import router as chunks_router
from ..models.document import Document, DocumentCreate, DocumentUpdate
from ..models.search import SearchRequest, SearchResult
from ..service.document_service import create_document_service, list_documents_service, get_document_service, update_document_service, delete_document_service

from ..service.search_service import search_document_service

from ..config import Config

import cohere

CO_API_KEY = Config.COHERE_KEY
co = cohere.ClientV2(api_key=CO_API_KEY)

router = APIRouter(
    prefix="/{library_id}/documents",
    tags=["chunks"],
)

router.include_router(chunks_router)

# simple in-memory store
# _fake_db: List[Document] = []

@router.post(
    "",
    response_model=Document,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Document",
)
async def create_document(
    library_id: UUID = Path(..., description="UUI of the library"),
    payload: DocumentCreate = Body(..., description="Metadata + Chunk ids")
) -> Document:
    try:
        return create_document_service(library_id,  payload)
    except KeyError:
        raise HTTPException(status_code=404, detail="Chunk not found in library")

@router.get(
    "",
    response_model=List[Document],
    status_code=status.HTTP_200_OK,
    summary="List all documents of a library",
)
async def list_documents(
    library_id: UUID = Path(..., description="UUID of the library")
) -> List[Document]:
    try:
        return list_documents_service(library_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Library not found")

@router.get(
    "/{document_id}",
    response_model=Document,
    status_code=status.HTTP_200_OK,
    summary="Get a document with library id and coument id",
)
async def get_document(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
) -> Document:
    try:
        return get_document_service(library_id, document_id)
    except:
        raise HTTPException(status=404, detail="Document not found")

@router.put(
    "/{document_id}",
    response_model=Document,
    status_code=status.HTTP_200_OK,
    summary="Update an existing document",
)
async def update_document(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
    payload: DocumentUpdate = Body(..., description="Field to update (all optional)"),
) -> Document:
    try:
        return update_document_service(library_id, document_id, payload)
    except KeyError:
        raise HTTPException(status_code=404, detail="Document and/or chunk not found")

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a document",
)
async def delete_document(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
) -> None:
    try:
        delete_document_service(library_id, document_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")

@router.post(
    "/{document_id}/search",
    response_model=List[SearchResult],
    status_code=status.HTTP_200_OK,
    summary="kNN search within a Document",
)
async def search_document(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
    payload: SearchRequest = Body(..., description="Search parameters")
) -> List[SearchResult]:
    """top-k most similar chunks within a specific document"""
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

        return search_document_service(
            library_id=library_id,
            document_id=document_id,
            query_embedding=payload.query_embedding,
            k=payload.k,
            metric=payload.metric,
            metadata_filter=payload.filter,
        )
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )