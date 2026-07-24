from typing import Sequence
from src.modules.notifications.models import Notification
from src.modules.notifications.schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from src.modules.notifications.repositories import INotificationRepository
from src.modules.notifications.adapters import NotificationAdapterFactory
from src.modules.notifications.exceptions import NotificationNotFoundError

class NotificationService:
    def __init__(self, repository: INotificationRepository):
        self.repository = repository

    async def send_and_create(self, dto: NotificationCreate, user_id: str) -> NotificationResponse:
        adapter = NotificationAdapterFactory.get_adapter(dto.channel)
        await adapter.send(recipient=dto.recipient, title=dto.title, content=dto.content)

        notification = Notification(
            title=dto.title,
            content=dto.content,
            channel=dto.channel,
            recipient=dto.recipient,
            user_id=user_id
        )
        saved = await self.repository.create(notification)
        return saved #NotificationResponse.model_validate(saved)

    async def get_user_notifications(self, user_id: str) -> list[NotificationResponse]:
        records = await self.repository.list_by_user(user_id)
        return [NotificationResponse.model_validate(item) for item in records]

    async def update_notification(self, notification_id: str, dto: NotificationUpdate, user_id: str) -> NotificationResponse:
        record = await self.repository.get_by_id(notification_id, user_id)
        if not record:
            raise NotificationNotFoundError()

        if dto.title is not None:
            record.title = dto.title
        if dto.content is not None:
            record.content = dto.content
        if dto.channel is not None:
            record.channel = dto.channel

        updated = await self.repository.update(record)
        return NotificationResponse.model_validate(updated)

    async def delete_notification(self, notification_id: str, user_id: str) -> None:
        record = await self.repository.get_by_id(notification_id, user_id)
        if not record:
            raise NotificationNotFoundError()
        await self.repository.delete(record)