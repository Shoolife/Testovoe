from fastapi import APIRouter, UploadFile, File, Depends
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db import models
from app.schemas.file import FileOut
from app.core.security import get_current_user
from app.db.models import User

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileOut)
async def upload_audio(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    audio_file = models.AudioFile(
        filename=file.filename, filepath=filepath, owner_id=current_user.id
    )
    db.add(audio_file)
    await db.commit()
    await db.refresh(audio_file)

    return FileOut(filename=audio_file.filename, filepath=audio_file.filepath)

@router.get("/", response_model=list[FileOut])
async def list_audio(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(models.AudioFile).where(models.AudioFile.owner_id == current_user.id)
    )
    audio_files = result.scalars().all()
    return [FileOut(filename=file.filename, filepath=file.filepath) for file in audio_files]