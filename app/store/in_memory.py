from threading import RLock
from typing import Dict, List, Optional
from uuid import UUID

from ..models.library import Library
from ..models.document import Document
from ..models.chunk import Chunk


# ----------------- in-memory ------------------
_lock = RLock()
_libraries: Dict[UUID, Library] = {}
_documents: Dict[UUID, Document] = {}
_chunks: Dict[UUID, Chunk] = {}


# ----------------- library related funciton ------------------

def save_library(lib: Library) -> None:
    with _lock:
        _libraries[lib.id] = lib

def get_library(library_id: UUID) -> Optional[Library]:
    with _lock:
        return _libraries.get(library_id)
    
def list_libraries() -> List[Library]:
    with _lock:
        return list(_libraries.values())

def delete_library(library_id: UUID) -> None:
    with _lock:
        # remove library
        _libraries.pop(library_id, None)
        # remove its documents
        for doc_id, doc in list(_documents.items()):
            if doc.library_id == library_id:
                _documents.pop(doc_id)

        # remove its chunks
        for chunk_id, chunk in list(_chunks.items()):
            if chunk.library_id == library_id:
                _chunks.pop(chunk_id)



# ----------------- document related funciton ------------------

def save_document(doc: Document) -> None:
    with _lock:
        _documents[doc.id] = doc

def get_document(document_id: UUID) -> Optional[Document]:
    with _lock:
        return _documents.get(document_id)
    
def list_documents(library_id: UUID) -> List[Document]:
    with _lock:
        return [doc for doc in _documents.values() if doc.library_id == library_id]
    
def delete_document(document_id: UUID) -> None:
    with _lock:
        _documents.pop(document_id, None)
        # remove its chunks
        for chunk_id, chunk in list(_chunks.items()):
            if chunk.document_id == document_id:
                _chunks.pop(chunk_id)



# ----------------- chunk related funciton ------------------

def save_chunk(chunk: Chunk) -> None:
    with _lock:
        _chunks[chunk.id] = chunk

def get_chunk(chunk_id: UUID) -> Optional[Chunk]:
    with _lock:
        return _chunks.get(chunk_id)
    
def list_chunks(library_id: UUID, document_id: UUID) -> List[Chunk]:
    with _lock:
        result = []
        for chunk in _chunks.values():
            print("chunk id: ", chunk.library_id)
            print("chunk document id: ", chunk.document_id)
            if chunk.library_id == library_id and chunk.document_id == document_id:
                result.append(chunk)

        print("result: ", result)
        return result
    
def delete_chunk(chunk_id: UUID) -> None:
    with _lock:
        _chunks.pop(chunk_id, None)

def list_all_chunks_in_library(library_id: UUID) -> List[Chunk]:
    with _lock:
        return [
            chunk
            for chunk in _chunks.values()
            if chunk.library_id == library_id
        ]


def add_chunk_to_document(
    chunk: Chunk, document_id: UUID
) -> None:
    with _lock:
        _chunks[chunk.id] = chunk
        doc = _documents[document_id]
        doc.chunk_ids.append(chunk.id)
        _documents[document_id] = doc


def remove_chunk_from_document(
    chunk_id: UUID, document_id: UUID
) -> None:
    with _lock:
        # remove the chunk record
        _chunks.pop(chunk_id, None)
        # remove the reference in the document
        doc = _documents[document_id]
        if chunk_id in doc.chunk_ids:
            doc.chunk_ids.remove(chunk_id)
            _documents[document_id] = doc



def list_all_chunks_in_library(library_id: UUID) -> List[Chunk]:
    with _lock:
        return [c for c in _chunks.values() if c.library_id == library_id]