import math
from typing import List, Tuple, Callable, Any
from uuid import UUID

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """dot(a,b) / (||a|| * ||b||)"""
    dot = 0.0
    sum_sq_a = 0.0
    sum_sq_b = 0.0
    for i in range(len(a)):
        x = a[i]
        y = b[i]
        dot += x * y
        sum_sq_a += x * x
        sum_sq_b += y * y

    if sum_sq_a == 0.0 or sum_sq_b == 0.0:
        return 0.0

    norm = math.sqrt(sum_sq_a) * math.sqrt(sum_sq_b)
    return dot/norm

def l2_distance(
    a: List[float],
    b: List[float],
) -> float:
    total = 0.0
    for i in range(len(a)):
        diff = a[i] - b[i]
        total += diff * diff

    return math.sqrt(total)


def brute_force_knn(
    query: List[float],
    candidates: List[Tuple[UUID, List[float], Any]],
    k: int,
    metric_fn,
) -> List[Tuple[UUID, float, Any]]:
    """score every candidate, sort, slice top-k"""

    scores: List[Tuple[UUID, float, Any]] = []

    for item in candidates:
        item_id, emb, payload = item
        score = metric_fn(query, emb)
        scores.append((item_id, score, payload))

    # higher score = better for cosine; lower = better for L2
    scores.sort(
        key=lambda triple: triple[1],
        reverse=(metric_fn is cosine_similarity)
    )

    result: List[Tuple[UUID, float, Any]] = []
    upper = k if k < len(scores) else len(scores)
    for i in range(upper):
        result.append(scores[i])
    return result

