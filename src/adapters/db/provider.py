from dishka import Provider, Scope, provide

from src.application.protocols import (
    DisposeComponentProtocol,
    InitComponentProtocol,
    WeatherRepositoryProtocol,
)

from .database import Database
from .repositories import WeatherRepository
from .settings import PostgresSettings


class PostgresProvider(Provider):
    component = "postgres"

    @provide(scope=Scope.APP)
    async def __init(self, db: Database) -> InitComponentProtocol:
        return InitComponentProtocol

    @provide(scope=Scope.APP)
    async def __dispose(self, db: Database) -> DisposeComponentProtocol:
        await db.dispose()
        return DisposeComponentProtocol

    @provide(scope=Scope.APP)
    async def __settings(self) -> PostgresSettings:
        return PostgresSettings()

    @provide(scope=Scope.APP)
    async def __database(self, settings: PostgresSettings) -> Database:
        return Database(settings)

    @provide(scope=Scope.APP)
    async def __weather(self, db: Database) -> WeatherRepositoryProtocol:
        return WeatherRepository(db)
