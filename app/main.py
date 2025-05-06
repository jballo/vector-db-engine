from fastapi import Depends, FastAPI

from .dependencies import get_key_header
from .routers import libraries
from .routers import documents
from .routers import chunks
from .routers import health

app = FastAPI(dependencies=[Depends(get_key_header)])

app.include_router(libraries.router)
# app.include_router(documents.router)
# app.include_router(chunks.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return { "message": "Hello from root!" }
