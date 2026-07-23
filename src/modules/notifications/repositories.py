from abc import ABC, abstractmethod
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.modules.notifications.models import Notification

class INotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:...
    @abstractmethod
    async def get_by_id(self,notification_id: str, user_id: str) -> Notification | None:...
    @abstractmethod
    async def list_by_user(self, user_id: str) -> Sequence[Notification]:...
    @abstractmethod
    async def update(self, notification: Notification) -> Notification:...
    @abstractmethod
    async def delete(self, notification: Notification) -> None:...

class SQLAlchemyNotificationRepository(INotificationRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, notification: Notification) -> Notification:
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification
    
    async def get_by_id(self, notification_id: str, user_id: str) -> Notification | None:
        result = await self.db.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id
            )
        )
        return result.scalars().first()
    
    async def list_by_user(self, user_id: str) -> Sequence[Notification]:
        result = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id)
        )
        return result.scalars().all()

    async def update(self, notification: Notification) -> Notification:
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def delete(self, notification: Notification) -> None:
        await self.db.delete(notification)
        await self.db.commit()

        