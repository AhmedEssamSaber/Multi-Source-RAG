from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.db.base import Base
from app.core.config import settings


import app.models.db.models  

engine = create_async_engine(
    settings.DATABASE_URL,
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

    from app.models.db.base import Base
    print("TABLES:", Base.metadata.tables.keys())  

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("DONE")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session