from datetime import datetime

from sqlalchemy import Index, func
from sqlalchemy.orm import Mapped, mapped_column

from src.application.utils.base import get_current_dt

from .base import Base


class WeatherData(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    date: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
    )
    temperature: Mapped[float]
    humidity: Mapped[float]

    __table_args__ = (Index("idx_weather_city_date", "city", "date"),)
