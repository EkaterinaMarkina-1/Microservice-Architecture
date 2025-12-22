#!/bin/bash
set -e

echo "Starting FastAPI with Uvicorn..."

# Проверка готовности БД через netcat
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

until nc -z -v -w30 $DB_HOST $DB_PORT
do
  echo "Waiting for database connection..."
  sleep 2
done

echo "Database is up. Starting app..."

# Запуск FastAPI
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

