from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str
    APP_HOST: str
    APP_PORT: int

    DEBUG: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    GATEWAY_URL: str
    DICTS_URL: str

    MAX_RETIRES: int = 5
    DEFAULT_BACKOFF: float = 5
    EXPONENT_FACTOR: float = 1.5
    MAX_BACKOFF: float = 20


class Settings(BaseServiceSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PG_DATABASE: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def POSTGRES_DSN(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SYNC_POSTGRES_DSN(self) -> str:
        return self.POSTGRES_DSN.replace("asyncpg", "psycopg2")


settings = Settings()  # type: ignore[call-arg]
