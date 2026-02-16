from pydantic import Field
from pydantic_settings import BaseSettings

from src.application.constants import DEFAULT_MAIN_API_ENV_PREFIX
from src.application.settings import set_model_config


class MSettings(BaseSettings):
    model_config = set_model_config(env_prefix=DEFAULT_MAIN_API_ENV_PREFIX)

    IS_DEV_MODE: bool = Field(default=False)

    ALLOW_ORIGINS: list[str] = Field(default=["*"], min_length=1)
    ALLOW_HEADERS: list[str] = Field(default=["*"], min_length=1)
    ALLOW_METHODS: list[str] = Field(default=["*"], min_length=1)

    IS_GZIP: bool = Field(default=True)
    GZIP_MIN_SIZE: int = Field(default=500, gt=100, lt=1024 * 10)
    GZIP_COMPRESS_LEVEL: int = Field(default=6, gt=0, le=9)
