import logging
from http import HTTPStatus
from typing import Any

import requests
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class WeatherDTO(BaseModel):
    city: str
    temperature: float
    humidity: float
    timezone: int


class OpenWeatherMapClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 10,
        max_retries: int = 3,
    ) -> None:
        if not api_key:
            msg = "API ключ не может быть пустым"
            raise ValueError(msg)

        self._base_url = base_url
        self._api_key = api_key
        self._timeout = timeout
        self._max_retries = max_retries

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "OpenWeatherMap-Airflow-Client/1.0",
            }
        )

        logger.info("Инициализирован клиент OpenWeatherMap")

    def close(self) -> None:
        if hasattr(self, "session"):
            self.session.close()

    def _make_request(
        self, endpoint: str, params: dict[str, Any]
    ) -> dict[str, Any] | None:
        url = f"{self._base_url}/{endpoint}"

        params.update({"appid": self._api_key, "units": "metric", "lang": "ru"})

        for attempt in range(self._max_retries):
            attempt_str = f"{attempt + 1}/{self._max_retries}"
            try:
                logger.debug(f"Запрос к {url} с параметрами: {params}")
                response = self.session.get(
                    url, params=params, timeout=self._timeout
                )
                response.raise_for_status()

                data = response.json()
                return data  # type: ignore[no-any-return]  # noqa

            except requests.exceptions.Timeout:
                logger.warning(f"Таймаут запроса (попытка {attempt_str})")

            except requests.exceptions.ConnectionError:
                logger.warning(f"Ошибка соединения (попытка {attempt_str})")

            except requests.exceptions.HTTPError as e:
                status_code = (
                    e.response.status_code if e.response else "unknown"
                )
                logger.exception(f"HTTP ошибка {status_code}")

                if status_code == HTTPStatus.UNAUTHORIZED:
                    logger.exception("Неверный API ключ")
                elif status_code == HTTPStatus.NOT_FOUND:
                    logger.exception("Эндпоинт не найден")
                elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
                    logger.exception("Превышен лимит запросов")

                return None

            except requests.exceptions.RequestException:
                logger.exception("Ошибка запроса")

            except ValueError:
                logger.exception("Ошибка парсинга JSON")

            if attempt == self._max_retries - 1:
                logger.error(
                    f"Превышено максимальное количество попыток для {url}"
                )
                return None

        return None

    def get_current_weather(self, lat: float, lon: float) -> WeatherDTO | None:
        params = {"lat": lat, "lon": lon}
        data = self._make_request("onecall", params)

        if not data:
            return None

        try:
            weather_info = {
                "city": data.get("name", "Unknown"),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "timezone": data.get("timezone", 0),
            }
            result = WeatherDTO(
                city=weather_info["city"],
                temperature=weather_info["temperature"],
                humidity=weather_info["humidity"],
                timezone=weather_info["timezone"],
            )

            logger.info(f"Успешно получены данные для {weather_info['city']}")
            return result  # noqa: TRY300

        except KeyError:
            logger.exception("Ошибка парсинга ответа: отсутствует ключ")
            return None
        except ValidationError:
            logger.exception("Ошибка валидации при сборке 'WeatherDTO'")
            return None
