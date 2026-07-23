from src.core.exceptions import BusinessException
from fastapi import status

class UserAlreadyExistsError(BusinessException):
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists", status_code=status.HTTP_400_BAD_REQUEST)

class InvalidCredentialsError(BusinessException):
    def __init__(self):
        super().__init__("Invalid email or password credentials", status_code=status.HTTP_401_UNAUTHORIZED)

class UserNotFoundError(BusinessException):
    def __init__(self):
        super().__init__("User account not found", status_code=status.HTTP_404_NOT_FOUND)