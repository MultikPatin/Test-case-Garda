from datetime import date, timedelta

from pydantic import BaseModel, Field

from src.application.helpers import date_now


def default_start_date() -> date:
    return date_now() - timedelta(weeks=1)


class WeatherFilters(BaseModel):
    start_date: date = Field(default_factory=default_start_date)
    end_date: date = Field(default_factory=date_now)
    city: str = Field(default="Moscow")


class WeatherDTO(BaseModel):
    id: int
    city: str
    date: date
    temperature: float
    humidity: float


class WeatherList(BaseModel):
    weather_list: list[WeatherDTO]


class WeatherStatistic(BaseModel):
    avg_temp: float
    avg_humidity: float
