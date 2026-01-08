from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import init_db
from src.routers import subscription as subscription_routes
from src.routes import user_routes


app = FastAPI(
    title="Users Service API",
    description="Отдельный микросервис для управления пользователями",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    root_path="/users"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_routes.router)

@app.get("/health", tags=["health"],
         summary="Проверить состояние сервиса", description="Возвращает статус работы сервиса.")
def health():
    return {"status": "ok"}