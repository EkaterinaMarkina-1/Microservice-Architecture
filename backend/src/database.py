import os
from typing import AsyncGenerator
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set for backend")

# Базовый класс для всех моделей backend
Base = declarative_base()

# Асинхронный движок для PostgreSQL
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Асинхронная сессия для Depends
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# Инициализация базы данных backend
async def init_db():
    """
    Создаёт таблицы Article, Comment, Tag, article_tags
    """
    try:
        from src.models.article import Article
        from src.models.comment import Comment
        from src.models.tag import Tag
        from src.models.association import article_tags 

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("Backend DB initialized")
    except SQLAlchemyError as e:
        print(f"Backend DB init error: {e}")
