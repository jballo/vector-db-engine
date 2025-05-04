from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_key_header

router = APIRouter(
    prefix="/health",
    tags=["health"],
    dependencies=[Depends(get_key_header)],
    responses={404: {"description": "Note found"}},
)

@router.get("")
async def health():
    return {"status": "ok"}