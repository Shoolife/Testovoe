from fastapi import FastAPI
from app.api import auth, files

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(files.router, prefix="/files", tags=["files"])