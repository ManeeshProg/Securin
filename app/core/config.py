from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Recipe API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Database settings
    DATABASE_URL: str = "sqlite:///./recipes.db"

    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
