from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.dependencies.database import get_db_session
from src.modules.users.models import User
from src.modules.users.repositories import SQLAlchemyUserRepository
from src.modules.users.services import UserService
from src.modules.notifications.repositories import SQLAlchemyNotificationRepository
from src.modules.notifications.services import NotificationService


def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    repo = SQLAlchemyUserRepository(db)
    return UserService(repo)

def get_notification_service(db: AsyncSession = Depends(get_db_session)) -> NotificationService:
    repo = SQLAlchemyNotificationRepository(db)
    return NotificationService(repo)