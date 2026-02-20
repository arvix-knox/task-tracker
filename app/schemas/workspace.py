from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime


class WorkspaceCreate(BaseModel):
    name: str
    key: str
    description: str | None = None


class WorkspaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class WorkspaceResponse(BaseModel):
    id: uuid.UUID
    name: str
    key: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)