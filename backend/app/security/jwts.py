from datetime import datetime, timedelta, timezone
from jose import jwt
import os

ALGO = "HS256"
SECRET = os.getenv("JWT_SECRET", "change-me")

def create_access_token(sub: str, expires_minutes: int = 60) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=expires_minutes)).timestamp())}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=[ALGO])
