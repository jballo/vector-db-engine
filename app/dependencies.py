from typing import Annotated
from fastapi import Header, HTTPException
# from app.config import Config
from .config import Config

api_key = Config.API_KEY

async def get_key_header(x_key: Annotated[str, Header()]):
    if x_key != api_key:
        raise HTTPException(status_code=400, detail="X-Key header invalid")