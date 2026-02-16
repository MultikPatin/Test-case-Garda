from datetime import date

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.application.constants import DEFAULT_POSTGRES_NAMING_CONVENTION
from src.application.helpers import camel_case_to_snake_case, date_now


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=DEFAULT_POSTGRES_NAMING_CONVENTION,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa
        return f"{camel_case_to_snake_case(cls.__name__)}s"


class WeatherData(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    date: Mapped[date] = mapped_column(default_factory=date_now)
    temperature: Mapped[float]
    humidity: Mapped[float]
