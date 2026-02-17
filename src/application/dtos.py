from datetime import datetime

from pydantic import BaseModel


class WeatherFilters(BaseModel):
    start_date: datetime
    end_date: datetime
    city: str


class WeatherDTO(BaseModel):
    id: int
    city: str
    date: datetime
    temperature: float
    humidity: float

    class Config:
        from_attributes = True


class WeatherList(BaseModel):
    weather_list: list[WeatherDTO]


class WeatherStatistic(BaseModel):
    avg_temp: float
    avg_humidity: float
