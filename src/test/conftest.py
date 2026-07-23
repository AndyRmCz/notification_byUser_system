import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient #, ASGILifespan
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from src.config.database import Base
from src.dependencies.database import get_db_session
# from src.dependencies.providers import get_current_user
from src.core.security import get_password_hash
from src.modules.users.models import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:" ## Change later for Docker test db

@pytest_asyncio.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session
        await session.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def seed_user(test_db_session: AsyncSession) -> User:
    user = User(
        id="user-test-id-123",
        email="developer@test.com",
        hashed_password="SecretPassword123"
    )
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    return user

@pytest_asyncio.fixture(scope="function")
async def client(test_db_session: AsyncSession, seed_user: User) -> AsyncGenerator[AsyncClient, None]:
    async def _override_db():
        yield test_db_session

    async def _override_current_user():
        return seed_user

    app.dependency_overrides[get_db_session] = _override_db
    # app.dependency_overrides[get_current_user] = _override_current_user

    # async with AsyncClient(transport=ASGILifespan(app), base_url="http://testserver") as ac:
    #     yield ac

    app.dependency_overrides.clear()