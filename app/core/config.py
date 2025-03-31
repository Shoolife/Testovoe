from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()