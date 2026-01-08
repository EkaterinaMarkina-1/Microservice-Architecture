# Используем официальный образ Python 3.11 slim
FROM python:3.11-slim

# Отключаем запись pyc и включаем буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
ENV PYTHONPATH=/app/src

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . .

# Делаем скрипт entrypoint исполняемым
RUN chmod +x entrypoint.sh

# Открываем порт приложения
EXPOSE 8000

# Точка входа
ENTRYPOINT ["./entrypoint.sh"]
