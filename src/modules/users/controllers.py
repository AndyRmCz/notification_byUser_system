from fastapi import APIRouter, Depends, status
from src.dependencies.providers import get_user_service
from src.modules.users.schemas import UserLoginRequest, UserRegisterRequest, UserResponse, TokenResponse
from src.modules.users.services import UserService

router = APIRouter(prefix="/auth", tags=["Authentication & Access"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Registerd a new user with email and password",
)
async def register(
    dto: UserRegisterRequest,
    service: UserService = Depends(get_user_service)
):
    return await service.register_user(dto)

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user",
    description="Validates credentials and returns an access token",
)
async def login(
    dto: UserLoginRequest,
    service: UserService = Depends(get_user_service)
):
    return await service.authenticate_user(dto)