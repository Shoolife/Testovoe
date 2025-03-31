import httpx
from app.core.config import settings

async def get_yandex_user(code: str):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post("https://oauth.yandex.ru/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.YANDEX_CLIENT_ID,
            "client_secret": settings.YANDEX_CLIENT_SECRET
        })
        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        user_resp = await client.get("https://login.yandex.ru/info?format=json", headers={
            "Authorization": f"OAuth {access_token}"
        })
        return user_resp.json()