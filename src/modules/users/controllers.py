from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from src.dependencies.providers import get_user_service
from src.modules.users.schemas import UserLoginRequest, UserRegisterRequest, UserResponse, TokenResponse
from src.modules.users.services import UserService

from sqlalchemy import func, select
from src.core.security import create_access_token, password_hash, oauth2_scheme, verify_access_token, verify_password
from src.config.settings import settings

from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.database import get_db_session
from src.modules.users.models import User


router = APIRouter(prefix="/auth", tags=["Authentication & Access"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Registers a new user with email and password",
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

@router.get("/me", response_model=UserResponse)
async def get_current_user(
        token:Annotated[str, Depends(oauth2_scheme)],
        service: UserService = Depends(get_user_service)
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # try:
    #     user_id_int = int(user_id)
    # except (TypeError, ValueError):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid or expired token",
    #         headers={"WWW_Authenticate": "Bearer"},
    #     )

    user = await service.get_authenticated_user(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401,
            detail="User not found",
            headers={"WWW_Authenticate": "Bearer"},
        )
    
    return user

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db_session)]
):
    result = await db.execute(
        select(User).where(
            User.email == form_data.username.lower(),
        ),
    )
    user = result.scalars().first()

    if not user or verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorret email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
        )
    return TokenResponse(access_token=access_token, token_type="bearer")