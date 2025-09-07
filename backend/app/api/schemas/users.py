from pydantic import BaseModel, EmailStr

class MeOut(BaseModel):
    id: int
    email: EmailStr
    name: str | None
    role: str
    timezone: str
    email_verified: bool
