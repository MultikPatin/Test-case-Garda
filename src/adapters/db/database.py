from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

if TYPE_CHECKING:
    from .settings import PostgresSettings


class Database:
    def __init__(self, settings: "PostgresSettings") -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=settings.dsn.encoded_string(),
            echo=settings.ECHO,
            echo_pool=settings.ECHO_POOL,
            pool_size=settings.POOL_SIZE,
            max_overflow=settings.MAX_OVERFLOW,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
