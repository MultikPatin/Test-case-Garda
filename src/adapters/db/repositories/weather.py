from typing import TYPE_CHECKING

from sqlalchemy import Numeric, and_, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.db.models import WeatherData
from src.application.dtos import (
    WeatherDTO,
    WeatherList,
    WeatherStatistic,
)

if TYPE_CHECKING:
    from src.adapters.db.database import Database
    from src.application.dtos import WeatherFilters


class WeatherRepository:
    def __init__(self, db: "Database") -> None:
        self._db = db

    async def get_all(self, filters: "WeatherFilters") -> WeatherList:
        session: AsyncSession = self._db.session_factory()

        try:
            stmt = (
                select(
                    WeatherData.id,
                    WeatherData.city,
                    WeatherData.date,
                    WeatherData.temperature,
                    WeatherData.humidity,
                )
                .where(
                    and_(
                        WeatherData.city == filters.city,
                        WeatherData.date >= filters.start_date,
                        WeatherData.date < filters.end_date,
                    )
                )
                .order_by(WeatherData.date)
            )

            result = await session.execute(stmt)
            rows = result.all()

            weather_list = [
                WeatherDTO(
                    id=row.id,
                    city=row.city,
                    date=row.date,
                    temperature=row.temperature,
                    humidity=row.humidity,
                )
                for row in rows
            ]

            return WeatherList(weather_list=weather_list)

        finally:
            await session.close()

    async def get_statistic(
        self, filters: "WeatherFilters"
    ) -> WeatherStatistic:
        session: AsyncSession = self._db.session_factory()

        try:
            stmt = (
                select(
                    WeatherData.city,
                    func.round(
                        func.avg(cast(WeatherData.temperature, Numeric(10, 2))),
                        1,
                    ).label("avg_temp"),
                    func.round(
                        func.avg(cast(WeatherData.humidity, Numeric(10, 2))), 1
                    ).label("avg_humidity"),
                )
                .where(
                    and_(
                        WeatherData.city == filters.city,
                        WeatherData.date >= filters.start_date,
                        WeatherData.date < filters.end_date,
                    )
                )
                .group_by(WeatherData.city)
            )

            result = await session.execute(stmt)
            row = result.first()

            if row:
                return WeatherStatistic(
                    avg_temp=row.avg_temp,
                    avg_humidity=row.avg_humidity,
                )
            return WeatherStatistic(
                avg_temp=0.0,
                avg_humidity=0.0,
            )
        finally:
            await session.close()
