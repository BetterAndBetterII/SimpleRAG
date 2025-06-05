import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SimpleRAG"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # LlamaIndex settings
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Load environment variables from .env file if it exists
settings = Settings()

