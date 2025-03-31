from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select
from app.db.session import get_db
from app.db import models
from app.schemas.user import UserUpdate, UserOut
from app.core.security import get_current_user, get_current_superuser

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def read_user_me(
    current_user: models.User = Depends(get_current_user),
):
    return UserOut.model_validate(current_user)


@router.patch("/me", response_model=UserOut)
async def update_user(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    stmt = (
        update(models.User)
        .where(models.User.id == current_user.id)
        .values(**update_data.dict(exclude_unset=True))
        .returning(models.User)
    )
    result = await db.execute(stmt)
    await db.commit()

    user_row = result.fetchone()
    user = user_row[0] if user_row else None

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut.model_validate(user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int = Path(..., description="ID пользователя для удаления"),
    db: AsyncSession = Depends(get_db),
    _: models.User = Depends(get_current_superuser),
):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.execute(delete(models.User).where(models.User.id == user_id))
    await db.commit()
