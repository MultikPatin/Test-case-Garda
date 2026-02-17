from datetime import datetime, timedelta
from typing import Self

from pydantic import BaseModel, Field, ValidationError, model_validator

from src.application.utils.base import get_current_dt


def default_start_date() -> datetime:
    return get_current_dt() - timedelta(weeks=1)


class WeatherFiltersRequest(BaseModel):
    start_date: datetime = Field(
        default_factory=default_start_date,
        description="Дата начало периода поиска",
    )
    end_date: datetime = Field(
        default_factory=get_current_dt,
        description="Дата окончания периода поиска",
    )
    city: str = Field(
        default="Moscow",
        description="Название города для поиска",
    )

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.end_date <= self.start_date:
            msg = "Start date must be before end date"
            raise ValidationError(msg)
        return self


class WeatherResponse(BaseModel):
    id: int = Field(description="Идентификатор записи")
    city: str = Field(description="Город в котором проводилось измерение")
    date: datetime = Field(description="Дата измерения")
    temperature: float = Field(description="Измеренная температура")
    humidity: float = Field(description="Измеренная влажность")


class WeatherListResponse(BaseModel):
    weather_list: list[WeatherResponse] = Field(
        description="Массив найденных измерений"
    )


class WeatherStatisticResponse(BaseModel):
    avg_temp: float = Field(
        description="Средняя температура на период в заданном городе"
    )
    avg_humidity: float = Field(
        description="Средняя влажность на период в заданном городе"
    )
