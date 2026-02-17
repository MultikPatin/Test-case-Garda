#!/usr/bin/env bash
set -e
if [ -z "$API_LOG_LEVEL" ]; then
  API_LOG_LEVEL=info
fi
if [ -z "$MAIN_API_PORT" ]; then
  MAIN_API_PORT=8000
fi

uv run alembic upgrade head
uv run uvicorn src.composites.weather:app --host 0.0.0.0 --port $MAIN_API_PORT --log-level $API_LOG_LEVEL --proxy-headers --forwarded-allow-ips '*'
