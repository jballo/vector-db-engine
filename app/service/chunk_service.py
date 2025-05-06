from uuid import uuid4, UUID
from typing import List

from ..models.chunk import Chunk, ChunkCreate, ChunkUpdate
from ..store.in_memory import get_library, get_document, save_chunk, get_chunk, list_chunks, add_chunk_to_document, remove_chunk_from_document

def create_chunk_service(
        library_id: UUID, document_id: UUID, payload: ChunkCreate
) -> Chunk:
    if get_library(library_id) is None:
        raise KeyError("Library not found")
    doc = get_document(document_id)
    if doc is None:
        raise KeyError("Document not found")
    
    chunk = Chunk(
        id=uuid4(),
        library_id=library_id,
        document_id=document_id,
        text=payload.text,
        embedding=payload.embedding,
        metadata=payload.metadata,
    )

    # save chunk and attach to parent document
    add_chunk_to_document(chunk, document_id)

    return chunk


def list_chunks_service(
    library_id: UUID, document_id: UUID
) -> List[Chunk]:
    if get_library(library_id) is None:
        raise KeyError("Library not found")
    doc = get_document(document_id)
    if doc is None:
        raise KeyError("Document not found")
    
    return list_chunks(library_id, document_id)


def get_chunk_service(
    library_id: UUID, document_id: UUID, chunk_id: UUID
) -> Chunk:
    doc_ = get_document
    chunk = get_chunk(chunk_id)
    if (
        chunk is None
        or chunk.library_id != library_id
        or chunk.document_id != document_id
    ):
        raise KeyError("Chunk not found")
    
    return chunk

def update_chunk_service(
    library_id: UUID, document_id: UUID, chunk_id: UUID, payload: ChunkUpdate
) -> Chunk:
    chunk = get_chunk_service(library_id, document_id, chunk_id)
    updated = chunk.model_copy(update=payload.model_dump(exclude_none=True))
    save_chunk(updated)
    return updated

def delete_chunk_service(
    library_id: UUID, document_id: UUID, chunk_id: UUID
) -> None:
    _ = get_chunk_service(library_id, document_id, chunk_id)
    # delete chunk and remove reference to parent document
    remove_chunk_from_document(chunk_id, document_id)
