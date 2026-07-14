from src.core.exceptions import BusinessException

class UserAlreadyExistsError(BusinessException):
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists", status_code=400)

class InvalidCredentialsError(BusinessException):
    def __init__(self):
        super().__init__("Invalid email or password credentials", status_code=401)

class UserNotFoundError(BusinessException):
    def __init__(self):
        super().__init__("User account not found", status_code=404)