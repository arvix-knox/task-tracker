from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_async_session
from app.models.user import User
from app.schemas.user import (
    AccessTokenResponse,
    RefreshTokenRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth import (
    login_user,
    logout_all_sessions,
    logout_user,
    refresh_access_token,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_async_session)):
    return await register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_async_session)):
    return await login_user(db, user_data)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(request: RefreshTokenRequest, db: AsyncSession = Depends(get_async_session)):
    return await refresh_access_token(db, request.refresh_token)


@router.post("/logout")
async def logout(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_session),
):
    return await logout_user(db, request.refresh_token)


@router.post("/logout-all")
async def logout_all(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    return await logout_all_sessions(db, current_user.id)
