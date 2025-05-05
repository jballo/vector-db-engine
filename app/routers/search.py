from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/{library_id}/search",
    tags=["search"],
)


@router.post("")
async def search_library():
    return {""}