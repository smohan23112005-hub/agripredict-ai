"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "AgriPredict AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./agripredict.db"
    FRONTEND_URL: str = "http://localhost:5173"

    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"
    DEMO_MODE: bool = False

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
