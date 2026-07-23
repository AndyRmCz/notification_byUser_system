from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env", 
        env_file_encoding = "utf-8",
        )

    DATABASE_URL: str      

    PROJECT_NAME: str = "Notification Management Platform"
    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    

    SECRET_KEY: SecretStr

settings = Settings()