import re
import logging
from datetime import datetime, timezone
from src.modules.notifications.clients import INotificationChannelAdapter
from src.modules.notifications.exceptions import NotificationDispatchError
from src.modules.notifications.models import NotificationChannel

logger = logging.getLogger("NotificationAdapters")

class EmailChannelAdapter(INotificationChannelAdapter):
    async def send(self, recipient:str, title:str, content: str) -> None:
        regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(regex, recipient):
            raise NotificationDispatchError(f"Invalid email address: {recipient}")
        template = f"[TEMPLATE] Subject: {title} | Body: {content}"
        logger.info(f"[EMAIL ADAPTER] Dispatched email to {recipient}: {template} ")

class SMSChannelAdapter(INotificationChannelAdapter):
    async def send(self, recipient: str, title: str, content: str) -> None:
        full_message = f"{title}: {content}"
        if len(full_message) > 160:
            raise NotificationDispatchError("SMS payload exceeds maximum allowable length of 160 characters.")
        now = datetime.now(timezone.utc).isoformat()
        logger.info(f"[SMS ADAPTER] Dispatched SMS to {recipient} at {now}: {full_message}")

class PushChannelAdapter(INotificationChannelAdapter):
    async def send(self, recipient: str, title: str, content: str) -> None:
        if not recipient or len(recipient) < 10:
            raise NotificationDispatchError("Invalid push device token identifier.")
        payload = {"title": title, "body": content, "device_token": recipient, "status": "SENT"}
        logger.info(f"[PUSH ADAPTER] Dispatched push payload: {payload}")

class NotificationAdapterFactory:
    """
    Factory providing dispatch strategy isolation.
    """
    _adapters: dict[NotificationChannel, INotificationChannelAdapter] = {
        NotificationChannel.EMAIL: EmailChannelAdapter(),
        NotificationChannel.SMS: SMSChannelAdapter(),
        NotificationChannel.PUSH: PushChannelAdapter(),
    }

    @classmethod
    def get_adapter(cls,channel: NotificationChannel) -> INotificationChannelAdapter:
        adapter = cls._adapters.get(channel)
        if not adapter:
            raise NotificationDispatchError(f"Unsopported channel strategy: {channel}")
        return adapter