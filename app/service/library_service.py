from uuid import uuid4, UUID
from typing import List

from ..models.library import Library, LibraryCreate, LibraryUpdate
from ..store.in_memory import save_library, get_library, list_libraries, delete_library


def create_library_service(payload: LibraryCreate) -> Library:
    lib = Library(id=uuid4(), **payload.model_dump())
    print("lib: ", lib)
    save_library(lib)

    return lib



def list_libraries_service() -> List[Library]:
    return list_libraries()



def get_library_service(library_id: UUID) -> Library:
    lib = get_library(library_id)
    
    if lib is None:
        raise KeyError("Library not found")
    
    return lib


def update_library_service(
    library_id: UUID, payload: LibraryUpdate
) -> Library:
    lib = get_library(library_id)
    
    if lib is None:
        raise KeyError("Library not found")
    
    updated = lib.model_copy(update=payload.model_dump(exclude_none=True))
    save_library(updated)
    
    return updated


def delete_library_service(library_id: UUID) -> None:
    if get_library(library_id) is None:
        raise KeyError("Library not found")
    
    delete_library(library_id)
