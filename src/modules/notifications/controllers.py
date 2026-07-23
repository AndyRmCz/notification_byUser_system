from fastapi import APIRouter, Depends, status, Path
from src.dependencies.providers import get_notification_service
from src.modules.users.models import User
from src.modules.notifications.schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from src.modules.notifications.services import NotificationService
from src.modules.users.controllers import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications Engine"])

@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dispatch & create notification",
    description="Triggers live message dispatch logic according to the selected channel, then logs the record upon delivery execution."
)
async def create_notification(
    dto: NotificationCreate,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
):
    return await service.send_and_create(dto, user_id=current_user.id)

@router.get(
    "/",
    response_model=list[NotificationResponse],
    summary="List caller's notifications",
    description="Fetches all created notifications belonging to the authenticated user."
)
async def list_notifications(
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
):
    return await service.get_user_notifications(user_id=current_user.id)

@router.patch(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Update notification content",
    description="Updates existing notification details without triggering re-transmission."
)
async def update_notification(
    notification_id: str = Path(..., description="Target UUID string"),
    dto: NotificationUpdate = ...,
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
):
    return await service.update_notification(notification_id, dto, user_id=current_user.id)

@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete notification record",
    description="Removes a specified notification record permanently."
)
async def delete_notification(
    notification_id: str = Path(..., description="Target UUID string"),
    current_user: User = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service)
):
    await service.delete_notification(notification_id, user_id=current_user.id)