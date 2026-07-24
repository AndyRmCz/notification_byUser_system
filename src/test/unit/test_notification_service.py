import pytest
from src.modules.notifications.models import Notification, NotificationChannel
from src.modules.notifications.schemas import NotificationCreate
from src.modules.notifications.repositories import INotificationRepository
from src.modules.notifications.services import NotificationService
from src.modules.notifications.exceptions import NotificationDispatchError

class FakeNotificationRepository(INotificationRepository):
    def __init__(self):
        self._items: dict[str, Notification] = {}

    async def create(self, notification: Notification) -> Notification:
        notification.id = f"notif-{len(self._items) + 1}"
        self._items[notification.id] = notification
        return notification

    async def get_by_id(self, notification_id: str, user_id: str) -> Notification | None:
        item = self._items.get(notification_id)
        return item if item and item.user_id == user_id else None

    async def list_by_user(self, user_id: str) -> list[Notification]:
        return [i for i in self._items.values() if i.user_id == user_id]

    async def update(self, notification: Notification) -> Notification:
        self._items[notification.id] = notification
        return notification

    async def delete(self, notification: Notification) -> None:
        self._items.pop(notification.id, None)

@pytest.mark.asyncio
async def test_send_email_notification_success():
    repo = FakeNotificationRepository()
    service = NotificationService(repo)
    dto = NotificationCreate(
        title="Welcome",
        content="Welcome to the platform!",
        channel=NotificationChannel.EMAIL,
        recipient="user@test.com"
    )

    res = await service.send_and_create(dto, user_id="user-1")

    assert res.id is not None
    assert res.channel == NotificationChannel.EMAIL

@pytest.mark.asyncio
async def test_send_sms_notification_exceeds_length_fails():
    repo = FakeNotificationRepository()
    service = NotificationService(repo)
    dto = NotificationCreate(
        title="Alert",
        content="X" * 165,
        channel=NotificationChannel.SMS,
        recipient="+1234567890"
    )

    with pytest.raises(NotificationDispatchError) as exc:
        await service.send_and_create(dto, user_id="user-1")

    assert "SMS payload exceeds maximum allowable length" in str(exc.value)