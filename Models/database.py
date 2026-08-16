import os

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)


# ==========================================
# DATABASE URL
# ==========================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set"
    )


# ==========================================
# ASYNC ENGINE
# ==========================================

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)


# ==========================================
# ASYNC SESSION
# ==========================================

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ==========================================
# BASE MODEL
# ==========================================

Base = declarative_base()


# ==========================================
# FASTAPI DATABASE DEPENDENCY
# ==========================================

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()