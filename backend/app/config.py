from pydantic import BaseModel
import os

class Settings(BaseModel):
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me")
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    DEFAULT_TIMEZONE: str = os.getenv("DEFAULT_TIMEZONE", "Asia/Nicosia")
    APP_BASE_URL: str = os.getenv("APP_BASE_URL", "http://localhost:8000")

settings = Settings()
