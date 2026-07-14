import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.main import app
from src.config.database import Base
from src.dependencies.database import get_db_session
from src.dependencies.providers import get_current_user
from src.core.security import get_password_hash
from src.modules.users.models import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:" ##C Change for docker test database

@pytest_asyncio.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session
        await session.close()
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def seed_user(test_db_session: AsyncSession, seed_user: User) -> AsyncGenerator[AsyncSession, None]:
    async def _override_db():
        yield test_db_session

    async def _override_current_user():
        yield seed_user

    app.dependency_override[get_db_session] = _override_db
    app.dependency_override[get_current_user] = _override_current_user

    app.dependency_override.clear()