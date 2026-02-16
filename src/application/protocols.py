from typing import TYPE_CHECKING, Any, Protocol

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


class InitComponentsProtocol(Protocol): ...


class InitComponentProtocol(Protocol): ...


class DisposeComponentsProtocol(Protocol): ...


class DisposeComponentProtocol(Protocol): ...


class MAppProtocol(Protocol):
    @property
    def api(self) -> Any: ...  # noqa: ANN401


class VAppProtocol(MAppProtocol, Protocol):
    @property
    def path(self) -> str: ...
