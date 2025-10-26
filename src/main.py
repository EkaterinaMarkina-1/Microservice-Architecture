from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db  # асинхронная инициализация базы
from src.routes import user_routes, article_routes, comment_routes, tag_routes

def create_app() -> FastAPI:
    """
    Фабрика приложения для масштабируемости.
    Позволяет создавать несколько экземпляров FastAPI,
    подключать middleware, роуты и инициализацию БД.
    """
    app = FastAPI(
        title="Blog Example API",
        description="Асинхронный блог на FastAPI с SQLAlchemy",
        version="1.0.0",
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # можно заменить на список доверенных доменов
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение роутов
    # Все роуты должны экспортировать объект `router`
    app.include_router(user_routes.router)
    app.include_router(article_routes.router)
    app.include_router(comment_routes.router)
    app.include_router(tag_routes.router)

    # Health-check роут
    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    # Роут по умолчанию
    @app.get("/", tags=["root"])
    async def root():
        return {"message": "API работает. Документация доступна по /docs"}

    # Асинхронная инициализация базы данных при старте
    @app.on_event("startup")
    async def on_startup():
        await init_db()

    return app


# Создаём экземпляр приложения
app = create_app()
