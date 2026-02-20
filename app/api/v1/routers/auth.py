from fastapi import APIRouter, Depends, HTTPException
from app.models import User
from app.db.base import Base
from app.db.session import get_async_session
from app.core.security import hash_password
from app.core.dependencies import get_current_user

