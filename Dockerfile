FROM python:3.11-slim

# Отключаем генерацию .pyc и включаем буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# ----------------------------
# Устанавливаем только необходимые системные зависимости
# Используем --no-install-recommends для экономии памяти
# ----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    libffi-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Копируем только requirements для кеширования слоев Docker
# ----------------------------
COPY requirements.txt .

# ----------------------------
# Обновляем pip и устанавливаем зависимости Python
# ----------------------------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Копируем весь проект в контейнер
# ----------------------------
COPY . .

# ----------------------------
# Делаем entrypoint исполняемым
# ----------------------------
RUN chmod +x entrypoint.sh

# ----------------------------
# Открываем порт
# ----------------------------
EXPOSE 8000

# ----------------------------
# Стартуем через entrypoint.sh
# ----------------------------
ENTRYPOINT ["./entrypoint.sh"]
