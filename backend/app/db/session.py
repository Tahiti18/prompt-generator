from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlalchemy import text
import os

# Raw DATABASE_URL from env (Railway often provides plain 'postgresql://...')
DATABASE_URL = os.getenv("DATABASE_URL", "")


def _to_async_url(url: str) -> str:
    """
    Ensure SQLAlchemy uses the async driver.
    Converts:
      - postgresql+psycopg2://...  -> postgresql+asyncpg://...
      - postgresql://...           -> postgresql+asyncpg://...
      - postgresql+asyncpg://...   -> unchanged
    """
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
    # Fail fast with a clear error instead of a cryptic async driver crash.
    raise RuntimeError(
        "DATABASE_URL is not set. Link your Railway Postgres and/or set DATABASE_URL env. "
        "Expected a value like 'postgresql://user:pass@host:5432/dbname'."
    )

# Create async engine/sessionmaker using asyncpg
async_engine: AsyncEngine = create_async_engine(ASYNC_URL, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    """FastAPI dependency that yields an AsyncSession."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_async_session():
    """Helper for scripts/tests to grab the session factory."""
    return AsyncSessionLocal()


async def healthcheck():
    """Simple DB ping used by /admin/health."""
    async with AsyncSessionLocal() as s:
        await s.execute(text("SELECT 1"))
        await s.commit()
