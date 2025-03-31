from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.db.session import get_db
from app.db import models
from app.schemas.user import UserOut
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()

class AdminLogin(BaseModel):
    login: str
    password: str

@router.post("/login")
async def admin_login(data: AdminLogin):
    if data.login == settings.ADMIN_LOGIN and data.password == settings.ADMIN_PASSWORD:
        token = create_access_token({"sub": "admin"}, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        return {"token": token}
    raise HTTPException(status_code=401, detail="Неверные данные")

@router.get("/users", response_model=list[UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(models.User.__table__.select())
    return [UserOut.model_validate(row) for row in result]

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(models.User.__table__.delete().where(models.User.id == user_id))
    await db.commit()
    return {"detail": "Пользователь удалён"}
