from src.core.security import get_password_hash, verify_password, create_access_token
from src.modules.users.models import User
from src.modules.users.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
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
            email = dto.email,
            hashed_password= get_password_hash(dto.password)
        )

        saved = await self.user_repo.create(user)
        return UserResponse.model_validate(saved)
    
    async def authenticate_user(self, dto: UserLoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(dto.email)
        if not user or not verify_password(dto.passwword, user.hashed_password):
            raise InvalidCredentialsError
        
        token = create_access_token(subject=user.email)
        return TokenResponse(access_token=token)