from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from src.modules.notifications.models import NotificationChannel

class NotificationBase(BaseModel):
    title: str = Field(..., description="Notification title summary", examples=["Security Alert"])
    content: str = Field(..., description="Message payload", examples=["New login detected from unusual IP."])
    channel: NotificationChannel = Field(..., description="Targer delivery strategy channel", examples=[NotificationChannel.EMAIL])
    recipient: str = Field(..., description="Recipient identifier (email, phone or token)", examples=["alerts@company.com"])

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    title: str | None = Field(None, description="Updated notification title", examples=["Resolved Security Alert"])
    content: str | None = Field(None, description="Updated notification body content", examples=["The security incident is closed."])

class NotificationResponse(NotificationBase):
    id: str = Field(..., examples=["b82d3345-d419-4cb5-8bd3-61e9da7c9450"])
    user_id: str = Field(..., examples=["550e8400-e29b-41d4-a716-446655440000"])
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )