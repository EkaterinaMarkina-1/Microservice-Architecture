from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# -------------------------
# Конфигурация базы данных
# -------------------------
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

# База для моделей
Base = declarative_base()

# Асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # лог SQL запросов
    future=True,
)

# Асинхронная сессия
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency для FastAPI
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# -------------------------
# Асинхронная инициализация
# -------------------------
async def init_db():
    """Создаёт все таблицы при старте приложения"""
    try:
        # Импорт моделей внутри функции, чтобы избежать циклического импорта
        from src.models import User, Article, Comment, Tag, article_tags

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("База данных инициализирована успешно!")
    except SQLAlchemyError as e:
        print(f"Ошибка при инициализации базы: {e}")
