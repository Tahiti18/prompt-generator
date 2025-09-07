from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from ..base import Base

class Ranking(Base):
    __tablename__ = "rankings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trend_item_id: Mapped[int] = mapped_column(ForeignKey("trend_items.id", ondelete="CASCADE"), index=True, nullable=False)
    global_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    per_topic_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
