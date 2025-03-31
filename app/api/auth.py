from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db import models
from app.schemas.token import Token
from app.services.yandex_oauth import get_yandex_user
from app.core import security, config

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def login():
    url = (
        f"https://oauth.yandex.ru/authorize?response_type=code&client_id={config.settings.YANDEX_CLIENT_ID}"
        f"&redirect_uri={config.settings.YANDEX_REDIRECT_URI}"
    )
    return RedirectResponse(url)

@router.get("/callback", response_class=HTMLResponse)
async def callback(request: Request, db: AsyncSession = Depends(get_db)):
    code = request.query_params.get("code")
    yandex_user = await get_yandex_user(code)
    yandex_id = yandex_user["id"]
    username = yandex_user.get("login", "unknown")

    result = await db.execute(
        models.User.__table__.select().where(models.User.yandex_id == yandex_id)
    )
    user = result.fetchone()

    if not user:
        user = models.User(yandex_id=yandex_id, username=username)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = security.create_access_token(
        {"sub": str(user.id)},
        config.settings.JWT_SECRET_KEY,
        config.settings.JWT_ALGORITHM,
    )

    return RedirectResponse(url=f"/profile?token={token}")
