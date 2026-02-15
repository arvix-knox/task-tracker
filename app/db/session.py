from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncGenerator
from app.config import settings
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_size=5, max_overflow=10)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
