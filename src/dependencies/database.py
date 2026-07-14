from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import AsyncSessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            session.close()