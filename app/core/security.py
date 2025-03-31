from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Header, HTTPException, Depends
from app.core import config
from app.db import models
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


def create_access_token(data: dict, secret: str, algorithm: str, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=algorithm)


async def get_current_user(
    authorization: str = Header(...), db: AsyncSession = Depends(get_db)
) -> models.User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    token = authorization[len("Bearer "):]
    try:
        payload = jwt.decode(
            token,
            config.settings.JWT_SECRET_KEY,
            algorithms=[config.settings.JWT_ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not a superuser")
    return current_user
