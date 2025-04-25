from pathlib import Path
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

@asynccontextmanager
async def session_connect(async_engine: AsyncEngine):
    """Context manager to create a session with the async engine."""
    async with (
        AsyncSession(async_engine, expire_on_commit=False) as session,
        session.begin()
    ):
        yield session

async def init_db(database_path: Path, *models: SQLModel):
    """Initialize the database and create tables for the provided models."""
    if database_path.exists():
        database_path.unlink()

    engine = create_async_engine(f"sqlite+aiosqlite:///{str(database_path.absolute())}", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with (
        AsyncSession(engine, expire_on_commit=False) as session,
        session.begin()
    ):
        for model in models:
            session.add(model)
        await session.commit()