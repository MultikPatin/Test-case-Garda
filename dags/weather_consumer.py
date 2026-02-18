import logging
import os
from datetime import datetime

from adapters.weather_api import OpenWeatherMapClient
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.python import PythonOperator
from stmt import CREATE_WEATHER_TABLE, INSERT_WEATHER_TABLE

logger = logging.getLogger("airflow.task")

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = os.getenv("OPENWEATHER_BASE_URL", "")
POSTGRES_CONN_ID = os.getenv("AIRFLOW_POSTGRES_CONN_ID")
SCHEDULE = "0 3 * * *"

CITIES = {
    "moscow": {"lat": 55.7558, "lon": 37.6176, "city_name": "moscow"},
    "london": {"lat": 51.5074, "lon": -0.1278, "city_name": "london"},
    "tokyo": {"lat": 35.6895, "lon": 139.6917, "city_name": "tokyo"},
}

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 2, 1),
    "retries": 1,
}


def fetch_city_weather(  # type: ignore[no-untyped-def]
    lat: float,
    lon: float,
    city_name: str,
    **context,  # noqa: ANN003
) -> None:
    client = OpenWeatherMapClient(base_url=BASE_URL, api_key=API_KEY)

    try:
        logger.info(f"Запрашиваю данные для lat: {lat}, lon: {lon}")
        weather_data = client.get_current_weather(lat=lat, lon=lon)

        if weather_data is None:
            msg = "Не получены данные с API"
            logger.error(msg)
            return

        context["ti"].xcom_push(
            key=f"weather_{city_name.lower()}", value=weather_data
        )
        logger.info(f"Успешно получены данные для {city_name}")

    except Exception:
        logger.exception(f"Ошибка при получении данных для {city_name}")
        return
    finally:
        client.close()


def create_table() -> None:
    PostgresHook(postgres_conn_id=POSTGRES_CONN_ID).run(CREATE_WEATHER_TABLE)
    logger.info("Убедились что таблица существует")


def save_results_to_postgres(**context) -> None:  # type: ignore[no-untyped-def] # noqa: ANN003
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)

    ti = context["ti"]
    successful_inserts = 0

    for city_key in CITIES:
        result = ti.xcom_pull(
            key=f"weather_{city_key.lower()}",
            task_ids=[f"fetch_{city_key}_weather"],
        )

        if result and isinstance(result, list) and result[0]:
            values = result[0]

            data = values.data

            hook.run(
                INSERT_WEATHER_TABLE,
                parameters=(
                    values.city,
                    data,
                    values.temperature,
                    values.humidity,
                ),
            )
            successful_inserts += 1
            logger.info(f"Сохранены данные для {data['city']} в Postgres")

    logger.info(f"Успешно сохранено {successful_inserts} записей в Postgres")


with DAG(
    dag_id="weather_dag",
    default_args=default_args,
    schedule=SCHEDULE,
    description="Получение погоды для городов",
    catchup=False,
    tags=["weather", "postgres", "storage"],
) as dag:
    check_postgres = PythonOperator(
        task_id="check_postgres_connection",
        python_callable=create_table,
    )

    fetch_moscow = PythonOperator(
        task_id="fetch_moscow_weather",
        python_callable=fetch_city_weather,
        op_kwargs=CITIES["moscow"],
    )

    fetch_london = PythonOperator(
        task_id="fetch_london_weather",
        python_callable=fetch_city_weather,
        op_kwargs=CITIES["london"],
    )

    fetch_tokyo = PythonOperator(
        task_id="fetch_tokyo_weather",
        python_callable=fetch_city_weather,
        op_kwargs=CITIES["tokyo"],
    )

    save_results = PythonOperator(
        task_id="save_results_to_postgres",
        python_callable=save_results_to_postgres,
    )

    check_postgres >> [fetch_moscow, fetch_london, fetch_tokyo] >> save_results
