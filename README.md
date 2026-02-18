## Стек технологий

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.40-4051B5?style=for-the-badge&logo=uvicorn&logoColor=white)
![Orjson](https://img.shields.io/badge/Orjson-3.11-8A2BE2?style=for-the-badge&logo=json&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-1.18-7F52FF?style=for-the-badge&logo=alembic&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Airflow-3.0-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.12-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Pydantic Settings](https://img.shields.io/badge/Pydantic_Settings-2.13-FFD43B?style=for-the-badge&logo=pydantic&logoColor=black)
![Dishka](https://img.shields.io/badge/Dishka-1.8-FF6B6B?style=for-the-badge&logo=python&logoColor=white)
![Uv](https://img.shields.io/badge/Uv-0.9.12-FFD43B?style=for-the-badge&logo=uv&logoColor=black)
![Ruff](https://img.shields.io/badge/Ruff-0.15-FB8B24?style=for-the-badge&logo=ruff&logoColor=white)
![Mypy](https://img.shields.io/badge/Mypy-1.19-2A6DB2?style=for-the-badge&logo=mypy&logoColor=white)
![Pre-commit](https://img.shields.io/badge/Pre--commit-4.5-FAB040?style=for-the-badge&logo=precommit&logoColor=white)

# Test-case-Garda

Проект сбора замеров температуры и влажности для городов: Москва, Лондон, Токио. Реализовано API для выдачи замеров и
средних значений за период для указанного города, а так же DAG на платформе Airflow, ежедневно собирающий данные из
openweather API.

## Установка зависимостей

Проект реализован с использованием пакетного менеджера uv.

```bash
uv sync --group dev
```

Работа c инструментами разработки описана в DEVELOPMENT.md.

## Запуск проекта

Не забудьте добавить файл .env с переменными окружения. Пример используемых описан в файле .env.example  
Проект запускается в едином docker-compose.yaml

Миграции накинуться автоматически при запуске всех сервисов, но вы можете в ручную применить миграции следующей командой

```bash
alembic upgrade head
```

Проверка конфигурации Airflow

```bash
docker compose run airflow-cli airflow config list
```

Инициализация Airflow

```bash
docker compose up airflow-init
```

Запуск всех сервисов

```bash
docker compose up -d
```

## Доступ к сервисам по умолчанию

Airflow UI: http://localhost:8080 (логин/пароль: airflow/airflow)

FastAPI Swagger: http://localhost:8000/api/v1/docs

PostgreSQL: localhost:5432 (пользователь: postgres, пароль: postgres)

## Структура DAG

#### DAG weather_dag_parallel_tasks выполняет следующие задачи:

- check_postgres_connection - проверка подключения к PostgreSQL
- fetch_moscow_weather - получение данных для Москвы
- fetch_london_weather - получение данных для Лондона
- fetch_tokyo_weather - получение данных для Токио

## FastAPI эндпоинты

#### GET /weather

Возвращает данные о погоде за указанный период для конкретного города.

Параметры:

- city (str) - название города
- start_date (str) - дата начала в формате YYYY-MM-DD
- end_date (str) - дата окончания в формате YYYY-MM-DD

Пример ответа:

```json
{
  "weather_list": [
    {
      "id": 1,
      "city": "London",
      "date": "2024-02-01",
      "temperature": -5.2,
      "humidity": 82
    },
    {
      "id": 2,
      "city": "London",
      "date": "2024-02-02",
      "temperature": -4.8,
      "humidity": 79
    }
  ]
}
```

#### GET /stats

Возвращает средние значения температуры и влажности за указанный период.

Параметры:

- city (str) - название города
- start_date (str) - дата начала в формате YYYY-MM-DD
- end_date (str) - дата окончания в формате YYYY-MM-DD

Пример ответа:

```json
{
  "city": "Лондон",
  "avg_temperature": 7.3,
  "avg_humidity": 76,
  "period": {
    "start": "2024-02-01",
    "end": "2024-02-07"
  }
}
```