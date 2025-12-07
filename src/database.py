from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def init_db():
    """Создаёт все таблицы при старте приложения"""
    try:
        from src.models import User, Article, Comment, Tag, article_tags  # импорт моделей здесь
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("База данных инициализирована успешно!")
    except SQLAlchemyError as e:
        print(f"Ошибка при инициализации базы: {e}")
