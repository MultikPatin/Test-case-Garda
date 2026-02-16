from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from src.application.dtos import WeatherFilters
from src.application.enums import URLEnum
from src.application.protocols import WeatherServiceProtocol

from .shemas import (
    WeatherFiltersRequest,
    WeatherListResponse,
    WeatherStatisticResponse,
)

router = APIRouter(route_class=DishkaRoute)


@router.get(
    URLEnum.root,
    summary="Возвращает данные за указанный диапазон дат и город",
    response_model=WeatherListResponse,
)
async def get_all(
    query: Annotated[
        WeatherFiltersRequest, Query(description="Набор параметров для поиска")
    ],
    service: FromDishka[WeatherServiceProtocol],
) -> WeatherListResponse:
    filters = WeatherFilters(**query.model_dump())
    result = await service.get_all(filters)
    return WeatherListResponse(**result.model_dump())


@router.get(
    "/stats",
    summary="Возвращает среднюю температуру и влажность "
    "за период для выбранного города",
    response_model=WeatherStatisticResponse,
)
async def get_statistic(
    query: Annotated[
        WeatherFiltersRequest, Query(description="Набор параметров для поиска")
    ],
    service: FromDishka[WeatherServiceProtocol],
) -> WeatherStatisticResponse:
    filters = WeatherFilters(**query.model_dump())
    result = await service.get_statistic(filters)
    return WeatherStatisticResponse(**result.model_dump())
