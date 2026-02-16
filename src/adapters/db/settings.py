from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings

from src.application.constants import (
    DEFAULT_DATABASE,
    DEFAULT_HOST,
    DEFAULT_PASSWORD,
    DEFAULT_POSTGRES_ENV_PREFIX,
    DEFAULT_POSTGRES_PORT,
    DEFAULT_POSTGRES_SCHEMA,
    DEFAULT_USERNAME,
)
from src.application.settings import set_model_config


class PostgresSettings(BaseSettings):
    model_config = set_model_config(env_prefix=DEFAULT_POSTGRES_ENV_PREFIX)

    HOST: str = Field(default=DEFAULT_HOST, min_length=1, max_length=255)
    PORT: int = Field(default=DEFAULT_POSTGRES_PORT, gt=0, lt=65536)
    USERNAME: str = Field(default=DEFAULT_USERNAME, max_length=255)
    PASSWORD: SecretStr = Field(default=DEFAULT_PASSWORD, max_length=255)
    SCHEMA: str = Field(
        default=DEFAULT_POSTGRES_SCHEMA, min_length=1, max_length=255
    )
    DATABASE: str = Field(
        default=DEFAULT_DATABASE, min_length=1, max_length=255
    )

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=self.SCHEMA,
            username=self.USERNAME,
            password=self.PASSWORD.get_secret_value(),
            host=self.HOST,
            port=self.PORT,
            path=self.DATABASE,
        )
