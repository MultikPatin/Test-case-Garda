from typing import TYPE_CHECKING

from .protocols import WeatherRepositoryProtocol

if TYPE_CHECKING:
    from .dtos import (
        WeatherFilters,
        WeatherList,
        WeatherStatistic,
    )


class WeatherService:
    def __init__(self, weather_repo: WeatherRepositoryProtocol) -> None:
        self._repo = weather_repo

    async def get_all(self, filters: "WeatherFilters") -> "WeatherList":
        return await self._repo.get_all(filters)

    async def get_statistic(
        self, filters: "WeatherFilters"
    ) -> "WeatherStatistic":
        return await self._repo.get_statistic(filters)
