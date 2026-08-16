from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "postgresql+asyncpg://my_fastapi_db_36ct_user:"
    "PASSWORD@dpg-da0t81fqj5pc73b871u0-a:5432/"
    "my_fastapi_db_36ct"
)

# Async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Async session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base model
Base = declarative_base()


# FastAPI dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()