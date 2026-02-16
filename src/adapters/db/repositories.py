from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.application.dtos import (
        WeatherFilters,
        WeatherList,
        WeatherStatistic,
    )

    from .database import Database


class WeatherRepository:
    def __init__(self, db: "Database") -> None:
        self._db = db

    async def get_all(self, filters: "WeatherFilters") -> "WeatherList":
        return WeatherList(weather_list=[])

    async def get_statistic(
        self, filters: "WeatherFilters"
    ) -> "WeatherStatistic":
        return WeatherStatistic(
            avg_temp=0,
            avg_humidity=0,
        )
