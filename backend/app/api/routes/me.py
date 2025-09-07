from fastapi import APIRouter, Depends
from app.deps import get_current_user
from app.api.schemas.users import MeOut
from app.db.models.users import User

router = APIRouter(tags=["me"])

@router.get("/me", response_model=MeOut)
async def me(user: User = Depends(get_current_user)):
    return MeOut(
        id=user.id, email=user.email, name=user.name, role=user.role,
        timezone=user.timezone, email_verified=user.email_verified
    )
