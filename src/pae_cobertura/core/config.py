# pae_cobertura/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pae_cobertura"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PAE Cobertura"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
