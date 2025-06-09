from pydantic import SecretStr
from pydantic_settings import BaseSettings as _BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from loguru import logger

from app.consts import env_file_path, env_file_encoding


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding=env_file_encoding,
        extra="ignore",
    )


class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_USER: str

    @property
    def url(self) -> URL:
        url: URL = URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )
        logger.info(f"Database URL: {url}")
        return url

    @property
    def test_url(self) -> str:
        url: str = 'sqlite+aiosqlite:///:memory:'
        return url


class Settings(BaseSettings):
    database_settings: DatabaseSettings = DatabaseSettings()


settings = Settings()
