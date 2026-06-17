from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    pg_host: str = Field(default="localhost")
    pg_port: int = Field(default=5432)
    pg_database: str = Field(default="postgres")
    pg_user: str = Field(default="postgres")
    pg_password: str = Field(default="root")
    max_retries: int = 3
    retry_backoff: float = 0.5

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
