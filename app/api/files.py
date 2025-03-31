from fastapi import APIRouter, UploadFile, File, Depends, Form
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db import models
from app.schemas.file import FileOut
from app.core.security import get_current_user
from app.db.models import User
from typing import Optional

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=FileOut)
async def upload_audio(
    file: UploadFile = File(...),
    custom_name: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _, ext = os.path.splitext(file.filename)

    if custom_name:
        if not os.path.splitext(custom_name)[1]:
            filename = custom_name + ext
        else:
            filename = custom_name
    else:
        filename = file.filename

    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    audio_file = models.AudioFile(
        filename=filename,
        filepath=filepath,
        owner_id=current_user.id,
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
