import uuid

from sqlalchemy import Boolean, DateTime, String, Text, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    frequency: Mapped[str] = mapped_column(String(20), server_default=text("'daily'"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()"),
        onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"Habit(id={self.id}, title={self.title}, frequency={self.frequency})"
    
class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    habit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    completion_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now()")
    )
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"HabitCompletion(id={self.id}, habit_id={self.habit_id}, completion_date={self.completion_date})"
