from dishka import AsyncContainer, Provider, make_async_container

from src.adapters.db import PostgresProvider

from .provider import ApplicationProvider


def make_core_container(
    scope_provider: Provider | None = None,
) -> AsyncContainer:
    providers: list[Provider] = [
        ApplicationProvider(),
        PostgresProvider(),
    ]
    if scope_provider is not None:
        providers.append(scope_provider)
    return make_async_container(*providers)
