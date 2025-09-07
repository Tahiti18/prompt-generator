from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# If DATABASE_URL uses psycopg2, we still want async engine; allow asyncpg URL alternatively
if DATABASE_URL and DATABASE_URL.startswith("postgresql+psycopg2"):
    # replace with asyncpg for SQLAlchemy async usage
    ASYNC_URL = DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")
else:
    ASYNC_URL = DATABASE_URL

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
