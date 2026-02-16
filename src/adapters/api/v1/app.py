from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.application.enums import URLEnum

from .controllers import router

if TYPE_CHECKING:
    from .settings import Settings


class App:
    def __init__(self, is_dev_mode: bool, settings: "Settings") -> None:
        self._path = settings.path
        docs_url = (
            None if settings.IS_STATIC_DOCS or not is_dev_mode else URLEnum.docs
        )

        self._api = FastAPI(
            default_response_class=ORJSONResponse,
            title=settings.TITLE,
            description=settings.DESCRIPTION,
            version=settings.version,
            docs_url=docs_url,
        )

        self._api.include_router(
            router=router,
            prefix="/weather",
            tags=["Weather"],
        )

    @property
    def api(self) -> FastAPI:
        return self._api

    @property
    def path(self) -> str:
        return self._path
