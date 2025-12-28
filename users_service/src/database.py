import os
from typing import AsyncGenerator
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set for users_service")

# Базовый класс для всех моделей
Base = declarative_base()

# Асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Генератор сессий для Depends
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# Инициализация базы данных
async def init_db():
    """
    Создаёт таблицы users при старте users_service
    """
    try:
        # Импорт всех моделей, чтобы SQLAlchemy знал о них
        from src.models.user import User

        async with engine.begin() as conn:
            # Создаём таблицы для всех моделей Base
            await conn.run_sync(Base.metadata.create_all)

        print("Users DB initialized")
    except SQLAlchemyError as e:
        print(f"Users DB init error: {e}")
