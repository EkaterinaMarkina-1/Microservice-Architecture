# Blog Platform API

RESTful API для блог-платформы с аутентификацией JWT, написанное на FastAPI.

## 🚀 Особенности

- **FastAPI** - современный высокопроизводительный фреймворк
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy** - ORM для работы с БД
- **JWT аутентификация** - безопасный доступ к API
- **Docker** - контейнеризация приложения
- **Soft Delete** - мягкое удаление статей и комментариев

## 📋 Требования

- Python 3.9+
- Docker & Docker Compose
- PostgreSQL

## 🛠 Установка и запуск

### Локальная разработка

1. **Клонирование репозитория:**

   ```bash
   git clone <repository-url>
   cd blog-platform
   ```

2. **Установка зависимостей:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка базы данных:**

   ```bash
   # Запуск PostgreSQL в Docker
   docker-compose up -d postgres

   # Применение миграций
   alembic upgrade head

   # Создание тестовых данных
   docker-compose exec app python -m src.scripts.seed_data
   ```

4. **Запуск приложения:**

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Docker (Production)

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Остановка
docker-compose down
```

## 🔐 Аутентификация

API использует JWT (JSON Web Tokens) для аутентификации:

1. Регистрация: POST /api/users
2. Авторизация: POST /api/users/login
3. Использование токена: Authorization: Bearer _token_

## 📚 API Документация

После запуска приложения доступны:

· Swagger UI: <http://localhost:8000/docs>
· ReDoc: <http://localhost:8000/redoc>
