# backend/app/routers/admin.py
from __future__ import annotations

import os
from fastapi import APIRouter
from sqlalchemy import create_engine, text

from app.db.base import Base
from app.db.session import healthcheck as async_healthcheck  # async ping for /admin/health

router = APIRouter(prefix="/admin", tags=["admin"])


def _to_sync_url(url: str) -> str:
    """
    Ensure metadata ops use a SYNC driver (psycopg2), not asyncpg.
    Converts:
      postgresql+asyncpg:// -> postgresql+psycopg2://
      postgresql://         -> postgresql+psycopg2://
    """
    if not url:
        return ""
    if url.startswith("postgresql+psycopg2"):
        return url
    if url.startswith("postgresql+asyncpg"):
        return url.replace("postgresql+asyncpg", "postgresql+psycopg2", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


@router.get("/health")
async def admin_health():
    ok = True
    try:
        await async_healthcheck()
    except Exception:
        ok = False
    return {"status": "ok", "db": ok}


@router.post("/bootstrap")
def admin_bootstrap():
    """
    Idempotently create all tables using SQLAlchemy metadata.
    Safe to run multiple times. No Alembic required for this step.
    """
    raw_url = os.getenv("DATABASE_URL", "")
    sync_url = _to_sync_url(raw_url)
    if not sync_url:
        return {"created": False, "error": "DATABASE_URL missing"}

    engine = create_engine(sync_url, pool_pre_ping=True, future=True)

    # Sanity ping
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Verify presence
    expected = [
        "users",
        "auth_identities",
        "interests",
        "sources",
        "trend_items",
        "rankings",
        "user_trend_scores",
        "prompts",
        "deliveries",
        "schedules",
        "audit_log",
    ]

    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname='public'")
        ).fetchall()
        present = sorted({r[0] for r in rows})

    return {"created": True, "tables_present": [t for t in expected if t in present]}
