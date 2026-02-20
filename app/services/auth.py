from datetime import timedelta

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status


async def register_user(db: AsyncSession, user_data: UserCreate):
    result = db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой пользователь уже существует")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,

    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def login_user(db: AsyncSession, user_data: UserLogin):
    result = db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    if not verify_password(user_data.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    access_token = create_access_token(data={"user_id": existing_user.id, "email": existing_user.email}, expires_delta=timedelta(minutes=30))

    refresh_token = create_refresh_token(data={"user.id": existing_user.id})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


async def refresh_access_token(db: AsyncSession, request):

    payload = decode_token(request.refresh_token)

    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный или истёкший refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Это не refresh token")

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некоррекнтый токен")

    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    new_access_token = create_access_token(
        data={"user_id": user.id,
              "email": user.email,
              },
        expires_delta=timedelta(minutes=30)
    )


    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


