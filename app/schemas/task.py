from datetime import datetime
import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TaskPriority = Literal["low", "medium", "high"]


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Short task title.",
        examples=["Finish quarterly report"],
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=3000,
        description="Detailed task description.",
        examples=["Prepare and send the report to the finance team."],
    )
    priority: TaskPriority = Field(
        default="medium",
        description="Task priority level.",
        examples=["high"],
    )
    due_date: datetime | None = Field(
        default=None,
        description="Task deadline in ISO 8601 format.",
        examples=["2026-03-01T18:00:00Z"],
    )


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title.",
        examples=["Finish quarterly report v2"],
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=3000,
        description="Updated task description.",
        examples=["Add final numbers before sharing with stakeholders."],
    )
    is_completed: bool | None = Field(
        default=None,
        description="Task completion status.",
        examples=[True],
    )
    priority: TaskPriority | None = Field(
        default=None,
        description="Updated task priority level.",
        examples=["low"],
    )
    due_date: datetime | None = Field(
        default=None,
        description="Updated deadline in ISO 8601 format.",
        examples=["2026-03-05T12:00:00Z"],
    )


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    is_completed: bool
    priority: TaskPriority
    due_date: datetime | None
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
