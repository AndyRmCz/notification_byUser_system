from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.modules.users.models import User

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: ...
    @abstractmethod
    async def create(self, user: User) -> User: ...