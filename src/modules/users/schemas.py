from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid user email address", examples=["user@domain.com"])
    password: str = Field(..., min_length=8, description="Strong account password", examples=["SecurePass123!"])

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["user@domain.com"])
    password: str = Field(..., examples=["SecurePass123!"])

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT bearer authentication token", examples=["eyJhbGciOiJIUzI1NiI..."])
    token_type: str = Field(default="bearer", examples=["bearer"])

class UserResponse(BaseModel):
    id: str = Field(..., examples=["550e8400-e29b-41d4-a716-446655440000"])
    email: EmailStr = Field(..., examples=["user@domain.com"])

    model_config = ConfigDict(
        from_attributes=True, 
        frozen=True
    )