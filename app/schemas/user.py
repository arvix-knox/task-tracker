from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    is_active: bool 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)