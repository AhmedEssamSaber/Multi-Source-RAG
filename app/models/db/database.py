from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.db.base import Base
import os

import app.models.db.models

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:ahmed1234@localhost:5432/postgres"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    print("INIT DB CALLED")

    async with engine.begin() as conn:
        print("METADATA TABLES:", Base.metadata.tables.keys())
        await conn.run_sync(Base.metadata.create_all)

    print("DONE")

        
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session