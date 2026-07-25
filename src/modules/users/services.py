from datetime import timedelta

from src.core.security import get_password_hash, verify_password, create_access_token
from src.config.settings import settings
from src.modules.users.models import User
from src.modules.users.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
)
from src.modules.users.repositories import IUserRepository
from src.modules.users.exceptions import UserAlreadyExistsError, InvalidCredentialsError


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def register_user(self, dto: UserRegisterRequest) -> UserResponse:
        existing = await self.user_repo.get_by_email(dto.email)
        if existing:
            raise UserAlreadyExistsError(dto.email)

        user = User(
            email=dto.email.lower(),
            hashed_password=get_password_hash(dto.password)
        )

        saved = await self.user_repo.create(user)
        return UserResponse.model_validate(saved)

    async def authenticate_user(self, dto: UserLoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(dto.email)
        if not user or not verify_password(dto.password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token_expires = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        return TokenResponse(access_token=token)

    async def get_authenticated_user(self, user_id: str) -> UserResponse:
        return await self.user_repo.get_by_id(user_id)
