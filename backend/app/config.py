from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Digital Yapper API"
    API_V1_STR: str = "/v1"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./conversations.db"
    
    # TODO: Microsoft Auth Configuration
    # AZURE_CLIENT_ID: str = ""
    # AZURE_CLIENT_SECRET: str = ""
    # AZURE_TENANT_ID: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
