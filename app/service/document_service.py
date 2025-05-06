from uuid import uuid4, UUID
from typing import List

from ..models.document import Document, DocumentCreate, DocumentUpdate
from ..store.in_memory import save_document, get_document, list_documents, delete_document, get_library, get_chunk, save_chunk


def create_document_service(
    library_id: UUID, payload: DocumentCreate
) -> Document:
    if get_library(library_id) is None:
        raise KeyError("Library not found")
    
    doc = Document(
        id=uuid4(),
        library_id=library_id,
        chunk_ids=[],
        metadata=payload.metadata,
    )
    save_document(doc)
    # attach existing chunks if chunk_ids supplied
    for chunk_id in payload.chunk_ids:
        chunk = get_chunk(chunk_id)
        if chunk is None or chunk.library_id != library_id:
            raise KeyError(f"Chunk {chunk_id} not found in library")
        chunk = chunk.model_copy(update={"document_id": doc.id})
        save_chunk(chunk)
        doc.chunk_ids.append(chunk.id)
    # persist updated doc with new chunk_ids
    save_document(doc)
    return doc


def list_documents_service(library_id: UUID) -> List[Document]:
    if get_library(library_id) is None:
        raise KeyError("Library not found")
    
    return list_documents(library_id)


def get_document_service(
    library_id: UUID, document_id: UUID
) -> Document:
    doc = get_document(document_id)
    if doc is None or doc.library_id != library_id:
        raise KeyError("Document not found")
    
    return doc

def update_document_service(
    library_id: UUID, document_id: UUID, payload: DocumentUpdate
) -> Document:
    doc = get_document_service(library_id, document_id)
    data = payload.model_dump(exclude_none=True)
    
    # handle chunk_ids change
    if "chunk_ids" in data:
        new_ids = data.pop("chunk_ids")
        # detach previous
        for chunk_id in doc.chunk_ids:
            if chunk_id not in new_ids:
                chunk = get_chunk(chunk_id)
                chunk = chunk.model_copy(update={"document_id": None})
                save_chunk(chunk)
        
        # attach new
        for chunk_id in new_ids:
            chunk = get_chunk(chunk_id)
            # ensures the chunk exists and that it is in this library
            if chunk is None or chunk.library_id != library_id:
                raise KeyError(f"Chunk {chunk_id} not found")
            chunk = chunk.model_copy(update={"document_id": document_id})
            save_chunk(chunk)

        data["chunk_ids"] = new_ids

    updated = doc.model_copy(update=data)
    save_document(updated)
    return updated

def delete_document_service(
    library_id: UUID, document_id: UUID
) -> None:
    _ = get_document_service(library_id, document_id)
    delete_document(document_id)