from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    pg_host: str = Field(default="localhost")
    pg_port: int = Field(default=5432)
    pg_db: str = Field(default="postgres")
    pg_user: str = Field(default="postgres")
    pg_password: str = Field(default="root")
    max_retries: int = 3
    retry_backoff: float = 0.5

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()





# class Settings(BaseSettings):
#     pg_host: str | None = None
#     pg_port: int | None = None
#     pg_db: str | None = None
#     pg_user: str | None = None
#     pg_password: str | None = None
#     max_retries: int = 3
#     retry_backoff: float = 0.5

#     class Config:
#         env_file = ".env"
#         extra = "allow"

# settings = Settings()



# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     pg_host: str
#     pg_port: int
#     pg_db: str
#     pg_user: str
#     pg_password: str
#     max_retries: int = 3
#     retry_backoff: float = 0.5

#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# settings = Settings()

