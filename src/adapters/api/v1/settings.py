from pydantic import Field
from pydantic_settings import BaseSettings

from src.application.constants import (
    DEFAULT_VERSIONED_API_DESCRIPTION,
    DEFAULT_VERSIONED_API_DESCRIPTION_LENGTH,
    DEFAULT_VERSIONED_API_TITLE,
    DEFAULT_VERSIONED_API_TITLE_LENGTH,
    WEATHER_API_ENV_PREFIX,
    WEATHER_API_VERSION,
)
from src.application.settings import get_versioned_prefix, set_model_config


class VSettings(BaseSettings):
    model_config = set_model_config(
        env_prefix=get_versioned_prefix(
            prefix=WEATHER_API_ENV_PREFIX,
            version=WEATHER_API_VERSION,
        )
    )

    TITLE: str = Field(
        default=DEFAULT_VERSIONED_API_TITLE,
        max_length=DEFAULT_VERSIONED_API_TITLE_LENGTH,
    )
    DESCRIPTION: str = Field(
        default=DEFAULT_VERSIONED_API_DESCRIPTION,
        max_length=DEFAULT_VERSIONED_API_DESCRIPTION_LENGTH,
    )

    MAJOR_VERSION: int = Field(default=1, gt=0, le=99)
    MINOR_VERSION: int = Field(default=0, ge=0, le=99)

    IS_STATIC_DOCS: bool = Field(default=True)

    @property
    def version(self) -> str:
        return f"{self.MAJOR_VERSION}.{self.MINOR_VERSION}"

    @property
    def path(self) -> str:
        return f"/v{self.MAJOR_VERSION}"
