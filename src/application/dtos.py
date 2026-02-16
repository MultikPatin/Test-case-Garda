from datetime import date

from pydantic import BaseModel


class WeatherFilters(BaseModel):
    start_date: date
    end_date: date
    city: str


class WeatherDTO(BaseModel):
    id: int
    city: str
    measurement_date: date
    temperature: float
    humidity: float


class WeatherList(BaseModel):
    weather_list: list[WeatherDTO]


class WeatherStatistic(BaseModel):
    avg_temp: float
    avg_humidity: float
