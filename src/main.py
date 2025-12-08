from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db
from src.routes import user_routes, article_routes, comment_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Blog API",
        description="API для управления пользователями, статьями и комментариями в блог-платформе.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user_routes.router)
    app.include_router(article_routes.router)
    app.include_router(comment_routes.router)

    @app.on_event("startup")
    async def startup_event():
        await init_db()

    return app


app = create_app()
