from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy import text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "")

def _to_async_url(url: str) -> str:
    if not url:
        return ""
    if url.startswith("postgresql+asyncpg"):
        return url
    if url.startswith("postgresql+psycopg2"):
        return url.replace("postgresql+psycopg2", "postgresql+asyncpg", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url

ASYNC_URL = _to_async_url(DATABASE_URL)

if not ASYNC_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Link Railway Postgres and/or set DATABASE_URL. "
        "Expected like 'postgresql://user:pass@host:5432/dbname'."
    )

async_engine: AsyncEngine = create_async_engine(ASYNC_URL, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_async_session():
    return AsyncSessionLocal()

async def healthcheck():
    async with AsyncSessionLocal() as s:
        await s.execute(text("SELECT 1"))
        await s.commit()
