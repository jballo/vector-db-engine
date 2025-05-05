from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from typing import List
from uuid import uuid4, UUID
from .chunks import router as chunks_router
from ..models.document import Document, DocumentCreate, DocumentUpdate
from ..models.search import SearchRequest, SearchResult

router = APIRouter(
    prefix="/{library_id}/documents",
    tags=["chunks"],
)

router.include_router(chunks_router)

# simple in-memory store
_fake_db: List[Document] = []

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
    doc = Document(id=uuid4(), library_id=library_id, **payload.model_dump())
    _fake_db.append(doc)
    return doc

@router.get(
    "",
    response_model=List[Document],
    status_code=status.HTTP_200_OK,
    summary="List all documents of a library",
)
async def list_documents(
    library_id: UUID = Path(..., description="UUID of the library")
) -> List[Document]:
    docs = [doc for doc in _fake_db if doc.library_id == library_id]
    return docs

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
    for doc in _fake_db:
        if doc.library_id == library_id and doc.id == document_id:
            return doc
    
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
    for idx, doc in enumerate(_fake_db):
        if doc.library_id == library_id and doc.id == document_id:
            updated = doc.model_copy(update=payload.model_dump(exclude_none=True))
            _fake_db[idx] = updated
            return updated
        
    raise HTTPException(status_code=404, detail="Document not found")

@router.delete(
    "/{document_id}",
    response_model=Document,
    status_code=status.HTTP_200_OK,
    summary="Delete a document",
)
async def delete_document(
    library_id: UUID = Path(..., description="UUID of the library"), 
    document_id: UUID = Path(..., description="UUID of the document"),
) -> Document:
    for idx, doc in enumerate(_fake_db):
        if doc.library_id == library_id and doc.id == document_id:
            return _fake_db.pop(idx)
        
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
    return []