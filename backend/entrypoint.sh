#!/bin/sh

# Ждем БД (опционально, если хочешь проверить доступность)
echo "PostgreSQL is up. Running migrations..."

# Запуск Alembic через python напрямую
# Предполагается, что alembic установлен через pip
alembic upgrade head

echo "Starting FastAPI..."
# Запуск приложения напрямую через uvicorn
exec python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
