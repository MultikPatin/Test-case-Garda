from dishka import AsyncContainer, Provider, Scope, from_context, provide
from dishka.integrations.fastapi import setup_dishka

from src.application.protocols import MAppProtocol

from . import v1
from .app import App
from .lifespan import lifespan
from .settings import MSettings


class ApiProvider(Provider):
    container = from_context(provides=AsyncContainer, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def __settings(self) -> MSettings:
        return MSettings()

    @provide(scope=Scope.APP)
    def __app(
        self, settings: MSettings, container: AsyncContainer, api_v1: v1.App
    ) -> MAppProtocol:
        app = App(settings, lifespan)
        setup_dishka(container=container, app=app.api)
        app.mount(api_v1)
        return app

    @provide(scope=Scope.APP)
    def __settings_v1(self) -> v1.Settings:
        return v1.Settings()

    @provide(scope=Scope.APP)
    def __api_v1(
        self, app_settings: MSettings, settings: v1.Settings
    ) -> v1.App:
        return v1.App(
            is_dev_mode=app_settings.IS_DEV_MODE,
            settings=settings,
        )
