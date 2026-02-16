from pydantic import SecretStr

SEPARATOR = "_"

DEFAULT_MODEL_SETTING_CONFIG = {
    "env_file": ".env",
    "env_file_encoding": "utf-8",
    "env_nested_delimiter": "__",
    "extra": "ignore",
}
DEFAULT_API_ROOT_PATH = "/api"
DEFAULT_MAIN_API_ENV_PREFIX = "MAIN_API_"
DEFAULT_VERSIONED_API_TITLE = "Please add api title"
DEFAULT_VERSIONED_API_TITLE_LENGTH = 128
DEFAULT_VERSIONED_API_DESCRIPTION = "Please add api description"
DEFAULT_VERSIONED_API_DESCRIPTION_LENGTH = 256

DEFAULT_HOST = "localhost"
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = SecretStr("")
DEFAULT_DATABASE = "default-database"

DEFAULT_POSTGRES_PORT = 5432
DEFAULT_POSTGRES_ENV_PREFIX = "POSTGRES_"
DEFAULT_POSTGRES_SCHEMA = "postgresql"


DEFAULT_POSTGRES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


WEATHER_API_ENV_PREFIX = "WEATHER_API_"
WEATHER_API_VERSION = 1
