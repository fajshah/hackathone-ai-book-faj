from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Physical AI & Humanoid Robotics Textbook API"
    debug: bool = False

    # Database
    database_url: str
    neon_database_url: Optional[str] = None

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_chunks"

    # Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"

    class Config:
        env_file = ".env"


settings = Settings()