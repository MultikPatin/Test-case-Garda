from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.application.utils.base import camel_case_to_snake_case

DEFAULT_POSTGRES_NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=DEFAULT_POSTGRES_NAMING_CONVENTION,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa
        return f"{camel_case_to_snake_case(cls.__name__)}s"
