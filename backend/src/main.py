from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.article_routes import router as article_router
from src.routers.comment_routes import router as comments_router

app = FastAPI(
    title="Simple Blog API",
    version="1.0.0",
    description="API для управления статьями и комментариями в блог-платформе.",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Routers ------------------
app.include_router(article_router)
app.include_router(comments_router)

# ------------------ Health ------------------
@app.get(
    "/health",
    tags=["health"],
    summary="Проверить состояние сервиса",
    description="Возвращает статус работы сервиса.",
)
def health():
    return {"status": "ok"}
