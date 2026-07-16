"""
Application configuration.

Reads environment variables (via python-dotenv) with sensible local
defaults so the project runs immediately with zero setup.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "PlantCare AI"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "plantcare-ai-dev-secret-change-in-production")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./plantcare.db")

    # Default seed account
    DEFAULT_ADMIN_EMAIL: str = "admin@plantcare.ai"
    DEFAULT_ADMIN_PASSWORD: str = "admin123"
    DEFAULT_ADMIN_NAME: str = "Rahul"

    SESSION_COOKIE_NAME: str = "plantcare_session"
    SESSION_MAX_AGE: int = 60 * 60 * 24 * 14  # 14 days


settings = Settings()
