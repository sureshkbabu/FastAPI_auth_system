from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

DATABASE_URL = (
    f"mysql+asyncmy://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}/"
    f"{settings.DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
