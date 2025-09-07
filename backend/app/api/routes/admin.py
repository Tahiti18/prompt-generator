from fastapi import APIRouter
from app.db.session import healthcheck

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/health")
async def health():
    try:
        import asyncio
        asyncio.get_event_loop()
    except RuntimeError:
        pass
    # ping DB
    import anyio
    try:
        anyio.run(healthcheck)
        db_ok = True
    except Exception as e:
        db_ok = False
    return {"status": "ok", "db": db_ok}
