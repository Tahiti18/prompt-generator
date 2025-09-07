import os
import asyncio
from datetime import datetime
from sqlalchemy import select
from backend.app.db.session import async_engine, get_async_session
from backend.app.db.models.users import User
from backend.app.security.password import get_password_context
import anyio

pwd = get_password_context()

async def ensure_user(session, email, name, role):
    result = await session.execute(select(User).where(User.email == email))
    u = result.scalar_one_or_none()
    if u:
        print(f"User exists: {email}")
        return u
    u = User(email=email, name=name, role=role, timezone="Asia/Nicosia",
             email_verified=True, password_hash=pwd.hash('changeme'))
    session.add(u)
    await session.commit()
    print(f"Created user: {email}")
    return u

async def main():
    async with get_async_session() as session:
        await ensure_user(session, "admin@example.com", "Admin", "admin")
        await ensure_user(session, "marwan@example.com", "Marwan", "user")

anyio.run(main)
print("Seed complete.")
