import math
from typing import List, Tuple, Callable, Any
from uuid import UUID

import heapq
import random

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




def build_vptree(
    items: List[Tuple[UUID, List[float], Any]],
    dist_fn: Callable[[List[float],List[float]], float]
):
    """
    Recursively build a VP-Tree node from items.
    Returns the root node.
    """
    if not items:
        return None

    # 1) pick a random vantage point
    idx = random.randrange(len(items))
    vp_id, vp_emb, vp_obj = items[idx]
    # remove VP from list
    rest = items[:idx] + items[idx+1:]
    if not rest:
        # leaf
        return VPTreeNode(vp_id, vp_emb, vp_obj, None, None, None)

    # 2) compute distances to VP
    dlist = [(dist_fn(vp_emb, emb), id_, emb, obj)
             for (id_, emb, obj) in rest]
    dlist.sort(key=lambda x: x[0])
    # 3) split on median
    m = len(dlist) // 2
    radius = dlist[m][0]
    inner_items = [(id_, emb, obj) for (_, id_, emb, obj) in dlist[:m]]
    outer_items = [(id_, emb, obj) for (_, id_, emb, obj) in dlist[m:]]

    # 4) recurse
    inner = build_vptree(inner_items, dist_fn)
    outer = build_vptree(outer_items, dist_fn)

    return VPTreeNode(vp_id, vp_emb, vp_obj, radius, inner, outer)


def vptree_knn(
    root,
    query: List[float],
    k: int,
    dist_fn: Callable[[List[float],List[float]], float]
) -> List[Tuple[UUID, float, Any]]:
    """
    Query the VP-Tree with the given query vector.
    Returns up to k nearest (id, distance, obj) sorted by distance asc.
    """
    if root is None:
        return []

    # max-heap of (-distance, id, obj)
    heap: List[Tuple[float, UUID, Any]] = []

    def search(node):
        if node is None:
            return
        d = dist_fn(query, node.embedding)
        # push/poll to keep top-k smallest d
        if len(heap) < k:
            heapq.heappush(heap, (-d, node.id, node.obj))
        else:
            # worst dist at top of max-heap
            if d < -heap[0][0]:
                heapq.heapreplace(heap, (-d, node.id, node.obj))

        # if leaf, done
        if node.radius is None:
            return

        # descend promising side first
        if d < node.radius:
            # inside ball
            search(node.inner)
            # maybe outside
            if len(heap) < k or d + (-heap[0][0]) >= node.radius:
                search(node.outer)
        else:
            # outside ball
            search(node.outer)
            # maybe inside
            if len(heap) < k or d - (-heap[0][0]) <= node.radius:
                search(node.inner)

    search(root)

    # unpack heap to list, sort by ascending distance
    results = [ (id_, -neg_d, obj) for (neg_d, id_, obj) in heap ]
    results.sort(key=lambda x: x[1])
    return results


class VPTreeNode:
    __slots__ = ("id", "embedding", "obj", "radius", "inner", "outer")
    def __init__(self, id, embedding, obj, radius, inner, outer):
        self.id = id
        self.embedding = embedding
        self.obj = obj
        self.radius = radius
        self.inner = inner
        self.outer = outer