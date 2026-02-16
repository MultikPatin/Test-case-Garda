from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from starlette.types import Lifespan

from src.application.constants import DEFAULT_API_ROOT_PATH

if TYPE_CHECKING:
    from src.application.protocols import VAppProtocol

    from .settings import MSettings


class App:
    def __init__(
        self,
        settings: "MSettings",
        lifespan: Lifespan[FastAPI] | None = None,
    ) -> None:
        self._api = FastAPI(
            default_response_class=ORJSONResponse,
            lifespan=lifespan,
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
            root_path=DEFAULT_API_ROOT_PATH,
        )
        self._api.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_headers=settings.ALLOW_HEADERS,
            allow_methods=settings.ALLOW_METHODS,
        )
        if settings.IS_GZIP:
            self._api.add_middleware(
                GZipMiddleware,
                minimum_size=settings.GZIP_MIN_SIZE,
                compresslevel=settings.GZIP_COMPRESS_LEVEL,
            )

    def mount(self, app: "VAppProtocol") -> None:
        self._api.mount(path=app.path, app=app.api)

    @property
    def api(self) -> FastAPI:
        return self._api
