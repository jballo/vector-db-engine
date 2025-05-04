from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_key_header

router = APIRouter(
    prefix="/libraries",
    tags=["libraries"],
    dependencies=[Depends(get_key_header)],
    responses={404: {"description": "Note found"}},
)

dummy_data = [
    {"id": 1, "name": "Info A", "content": "context X"},
    {"id": 2, "name": "Info B", "content": "context Y"},
    {"id": 3, "name": "Info C", "content": "context Z"},
]

@router.get("")
async def read_libraries():
    return dummy_data