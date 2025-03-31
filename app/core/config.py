from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Яндекс OAuth
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    # JWT
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"

    # БД
    DATABASE_URL: str

    # Админ
    ADMIN_LOGIN: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    class Config:
        env_file = ".env"

settings = Settings()
