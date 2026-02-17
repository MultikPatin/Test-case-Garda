# ==== base uv ====
ARG UV_VERSION=latest

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# ==== base python ====
FROM python:3.12-slim AS base

COPY --from=uv /uv /bin/uv

# ==== Builder stage ====
FROM base AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Создаем виртуальное окружение и устанавливаем зависимости
RUN uv sync --frozen --no-install-project --no-dev

# ==== Runtime stage ====
FROM base

WORKDIR /app

# Копируем виртуальное окружение с правами
COPY --from=builder --chown=1000:1000 /app/.venv .venv

ENV  PYTHONDONTWRITEBYTECODE=1  PYTHONUNBUFFERED=1

# Обновляем минимальные зависимости (закрывает vulnerabilities)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя
RUN useradd -m -u 1000 appuser

COPY --chown=1000:1000 src/ ./src/
COPY --chown=1000:1000 ./alembic.ini .
COPY --chown=1000:1000 ./entrypoint.sh .

RUN chmod +x ./entrypoint*.sh

USER appuser

CMD ["./entrypoint.sh"]
