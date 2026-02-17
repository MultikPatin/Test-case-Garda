from typing import Annotated

from dishka import FromComponent, Provider, Scope, provide

from .protocols import (
    DisposeComponentProtocol,
    DisposeComponentsProtocol,
    InitComponentProtocol,
    InitComponentsProtocol,
    WeatherRepositoryProtocol,
    WeatherServiceProtocol,
)
from .service import WeatherService

database = "postgres"


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def __init(
        self,
        postgres: Annotated[InitComponentProtocol, FromComponent(database)],
    ) -> InitComponentsProtocol:
        return InitComponentsProtocol

    @provide(scope=Scope.APP)
    async def __dispose(
        self,
        postgres: Annotated[DisposeComponentProtocol, FromComponent(database)],
    ) -> DisposeComponentsProtocol:
        return DisposeComponentsProtocol

    @provide(scope=Scope.APP)
    def __weather(
        self,
        repo: Annotated[WeatherRepositoryProtocol, FromComponent(database)],
    ) -> WeatherServiceProtocol:
        return WeatherService(repo)
