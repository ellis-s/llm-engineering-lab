# from pydantic import BaseSettings

# class Settings(BaseSettings):

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "llm-engineering-lab"
    app_env: str = "local"
    debug: bool = False
    api_timeout_seconds: float = Field(default=30, gt=0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def load_settings() -> Settings:
    return Settings()
