from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Physical AI & Humanoid Robotics Textbook API"
    debug: bool = False

    # Server Configuration
    port: int = 8000
    node_env: str = "development"

    # Google API Configuration
    google_api_key: str = ""

    # Database
    database_url: str
    neon_database_url: Optional[str] = None
    mongodb_uri: Optional[str] = None

    # JWT Configuration
    jwt_secret: str = "your-super-secret-jwt-key-change-in-production"
    jwt_expires_in: str = "7d"

    # Rate Limiting
    rate_limit_window_ms: str = "15 * 60 * 1000"  # 15 minutes
    rate_limit_max_requests: int = 100

    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://localhost:3001,https://hackathone-ai-book-faj-511b.vercel.app,https://hackathone-ai-book-faj.vercel.app"

    # Qdrant
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "physical_ai"

    # Authentication
    secret_key: str = "your-super-secret-jwt-key-change-in-production"  # Default value
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o"

    # OpenRouter Configuration (alternative to OpenAI)
    openrouter_api_key: Optional[str] = None
    openrouter_model: str = "openai/gpt-4o"

    # Qwen API Configuration
    qwen_api_key: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()