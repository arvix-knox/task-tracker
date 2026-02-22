from datetime import datetime, timedelta
from app.models.refresh_token import RefreshToken

async def login_user(
    db: AsyncSession, 
    user_data: UserLogin,
    device_info: str | None = None,
    ip_address: str | None = None
) -> dict:
    """Логин пользователя"""
    
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    refresh_token, jti = create_refresh_token(data={"sub": str(user.id)})
    
    # Сохраняем refresh token в БД
    db_refresh_token = RefreshToken(
        token_jti=jti,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        device_info=device_info,
        ip_address=ip_address,
    )
    
    db.add(db_refresh_token)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> dict:
    """Обновление access токена с проверкой в БД"""
    
    payload = decode_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или истёкший refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Это не refresh token"
        )

    jti = payload.get("jti")
    user_id = payload.get("sub")
    
    if not jti or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен"
        )

    # Проверяем токен в БД
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_jti == jti,
            RefreshToken.revoked_at.is_(None),
        )
    )
    stored_token = result.scalar_one_or_none()

    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отозван или не существует"
        )

    # Проверяем, не истёк ли токен
    if stored_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token истёк"
        )

    # Проверяем пользователя
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден или деактивирован"
        )

    # Выдаём новый access token
    new_access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


async def logout_user(db: AsyncSession, refresh_token: str) -> dict:
    """Logout — отзыв refresh токена"""
    
    payload = decode_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный refresh token"
        )
    
    jti = payload.get("jti")
    
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token_jti == jti)
    )
    stored_token = result.scalar_one_or_none()
    
    if stored_token and stored_token.revoked_at is None:
        stored_token.revoked_at = datetime.utcnow()
        await db.commit()
    
    return {"message": "Logged out successfully"}


async def logout_all_sessions(db: AsyncSession, user_id: uuid.UUID) -> dict:
    
    
    await db.execute(
        update(RefreshToken)
        .where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None)
        )
        .values(revoked_at=datetime.utcnow())
    )
    
    await db.commit()
    
    return {"message": "All sessions logged out"}