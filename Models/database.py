from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://my_fastapi_db_36ct_user:shamsay321!@dpg-da0t81fqj5pc73b871u0-a:5432/my_fastapi_db_36ct"

# Create asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create asynchronous session
AsyncSessionLocal = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

# Base model
Base = declarative_base()

# Dependency function kwa FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()