from typing import Any

from pydantic_settings import SettingsConfigDict

from .constants import DEFAULT_MODEL_SETTING_CONFIG, SEPARATOR


def set_model_config(**kwargs: Any) -> SettingsConfigDict:  # noqa: ANN401
    for k in DEFAULT_MODEL_SETTING_CONFIG:
        if k not in kwargs:
            kwargs[k] = DEFAULT_MODEL_SETTING_CONFIG[k]
    return SettingsConfigDict(**kwargs)  # type: ignore


def get_versioned_prefix(prefix: str, version: int) -> str:
    if not prefix.endswith(SEPARATOR):
        prefix = prefix + SEPARATOR
    return f"{prefix}API{SEPARATOR}V{version}{SEPARATOR}"
