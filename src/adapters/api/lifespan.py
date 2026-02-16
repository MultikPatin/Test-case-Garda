from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from src.application.protocols import (
    DisposeComponentsProtocol,
    InitComponentsProtocol,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI") -> "AsyncGenerator[None, None]":
    await app.state.dishka_container.get(InitComponentsProtocol)
    yield
    await app.state.dishka_container.get(DisposeComponentsProtocol)
    await app.state.dishka_container.close()
