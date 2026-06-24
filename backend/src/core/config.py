from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="postgresql://lablex_admin:lablex_password@localhost:5432/lablex_db")
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    MINIO_ENDPOINT: str = Field(default="localhost:9000")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin")
    MINIO_SECRET_KEY: str = Field(default="minioadmin")
    MINIO_BUCKET_NAME: str = Field(default="lablex-artifacts")
    
    JWT_SECRET: str = Field(default="supersecretjwtkeyforlocaldevelopment12345!")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    
    # Must be 32 bytes for AES-256-GCM local development mode KEK
    ENCRYPTION_KEY: str = Field(default="local-dev-kek-key-32-chars-long123")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
