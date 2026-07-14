from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Notification Management Platform"
    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()