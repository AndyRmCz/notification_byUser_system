from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings
from src.dependencies.database import get_db_session
from src.modules.users.models import User
from src.modules.users.repositories import SQLAlchemyUserRepository
from src.modules.users.services import UserService
# from src.modules.notifications.repositories import SQLAlchemyNotificationRepository
# from src.modules.notifications.services import NotificationService

oauth_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    repo = SQLAlchemyUserRepository(db)
    return UserService(repo)

# def get_notification_service(db: AsyncSession = Depends(get_db_session)) -> NotificationService:
#     repo = SQLAlchemyNotificationRepository(db)
#     return NotificationService(repo)

async def get_current_user(
    token: str = Depends(oauth_scheme),
    db: AsyncSession = Depends(get_db_session)
) -> User:
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authorization bearer credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.encode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise unauthorized_exc
    except JWTError:
        raise unauthorized_exc
    
    user_repo = SQLAlchemyUserRepository(db)
    user = user_repo.get_by_email(email)
    if user is None:
        raise unauthorized_exc
    return user