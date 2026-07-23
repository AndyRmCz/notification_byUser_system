from src.core.exceptions import BusinessException

class NotificationNotFoundError(BusinessException):
    def __init__(self):
        super().__init__("Notification record not found or Unauthorized", status_code=404)

class NotificationDispatchError(BusinessException):
    def __init__(self, reason: str):
        super().__init__(f"Notifiation dispatch failed: {reason}", status_code=400)