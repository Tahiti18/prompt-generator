from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.config import settings
from app.logging import setup_logging
from app.security.rate_limit import limiter
from app.api.routes import auth as auth_routes
from app.api.routes import me as me_routes
from app.api.routes import admin as admin_routes

setup_logging()
app = FastAPI(title="Trend App API", version="0.1.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda r, e: ({"detail": "Rate limit exceeded"}, 429))
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(me_routes.router)
app.include_router(admin_routes.router)

@app.get("/")
def root():
    return {"ok": True, "name": "trend-backend"}
