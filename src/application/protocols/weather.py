from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.application.dtos import (
        WeatherFilters,
        WeatherList,
        WeatherStatistic,
    )


class WeatherRepositoryProtocol(Protocol):
    async def get_all(self, filters: "WeatherFilters") -> "WeatherList": ...

    async def get_statistic(
        self, filters: "WeatherFilters"
    ) -> "WeatherStatistic": ...


class WeatherServiceProtocol(Protocol):
    async def get_all(self, filters: "WeatherFilters") -> "WeatherList": ...

    async def get_statistic(
        self, filters: "WeatherFilters"
    ) -> "WeatherStatistic": ...
