from fastapi import APIRouter, UploadFile, File, Depends
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db import models
from app.schemas.file import FileOut

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileOut)
async def upload_audio(user_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    audio_file = models.AudioFile(filename=file.filename, filepath=filepath, owner_id=user_id)
    db.add(audio_file)
    await db.commit()
    await db.refresh(audio_file)

    return FileOut(filename=audio_file.filename, filepath=audio_file.filepath)

@router.get("/", response_model=list[FileOut])
async def list_audio(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(models.AudioFile.__table__.select().where(models.AudioFile.owner_id == user_id))
    return [FileOut(filename=row.filename, filepath=row.filepath) for row in result]