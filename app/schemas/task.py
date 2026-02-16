from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: str = "medium"
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
    priority: str | None = None
    due_date: datetime | None = None

class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    is_completed: bool
    priority: str
    due_date: datetime | None
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
     
    model_config = ConfigDict(from_attributes=True)