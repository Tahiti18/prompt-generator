from datetime import datetime
from sqlalchemy import String, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from ..base import Base

class Interest(Base):
    __tablename__ = "interests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    tag: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    source_hint: Mapped[str | None] = mapped_column(String(128), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
