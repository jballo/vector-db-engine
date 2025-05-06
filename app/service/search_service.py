from uuid import uuid4, UUID
from typing import List, Tuple, Callable
from ..models.search import SearchResult
from ..store.in_memory import list_all_chunks_in_library, list_chunks
from ..utils.knn import brute_force_knn, cosine_similarity, l2_distance
from ..models.chunk import Chunk


def search_library_service(
    library_id: UUID,
    query_embedding: List[float],
    k: int,
    metric: str = "cosine",
    metadata_filter: dict = None,
) -> List[SearchResult]:
    candidates = list_all_chunks_in_library(library_id)
    if not candidates:
        return []
    
    return _run_knn(candidates, query_embedding, k, metric, metadata_filter)


def search_document_service(
    library_id: UUID,
    document_id: UUID,
    query_embedding: List[float],
    k: int,
    metric: str = "cosine",
    metadata_filter: dict = None,
) -> List[SearchResult]:
    candidates = list_chunks(library_id, document_id)
    print("candidates: ", candidates)
    if not candidates:
        return []
    
    return _run_knn(candidates, query_embedding, k, metric, metadata_filter)


def _run_knn(
    chunks: List[Chunk],
    query_embedding: List[float],
    k: int,
    metric: str,
    metadata_filter: dict = None,
) -> List[SearchResult]:
    # exact match metadata filter
    # if metadata_filter:
    #     chunks = [
    #         chunk for chunk in chunks
    #         if all(c.metadata.get(k_) == v_ for k_, v_ in metadata_filter.items())
    #     ]

    metric_fn: Callable = cosine_similarity if metric == "cosine" else l2_distance

    prepared = [(chunk.id, chunk.embedding, chunk) for chunk in chunks]

    raw_hits = brute_force_knn(query_embedding, prepared, k, metric_fn)
    print("raw_hits: ", raw_hits)

    return [
        SearchResult(chunk=chunk, score=score)
        for _, score, chunk in raw_hits
    ]

