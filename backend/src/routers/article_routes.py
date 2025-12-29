from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import get_current_user_id
from src.schemas.common import PaginatedResponse, PaginationMeta
from src.schemas.article_schemas import ArticleCreate, ArticleUpdate, ArticleOut, ArticleListItem

from src.controllers import article_controller as ctrl
from src.database import get_async_session

router = APIRouter(prefix="/api/articles", tags=["Articles"])

# ------------------ CREATE ARTICLE ------------------
@router.post(
    "/",
    response_model=ArticleOut,
    status_code=201,
    summary="Создание статьи",
    description="Создает новую статью и связывает её с текущим пользователем."
)
async def create_article(
    data: ArticleCreate,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id) 
):
    article = await ctrl.create_article(
        db,
        user_id,
        data.title,
        data.description,
        data.body,
        data.tagList
    )
    return ArticleOut.model_validate(article)


# ------------------ LIST ARTICLES (с пагинацией) ------------------
@router.get(
    "/",
    response_model=PaginatedResponse[ArticleListItem],
    summary="Список статей",
    description="Возвращает список статей с поддержкой пагинации."
)
async def list_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=50),
    db: AsyncSession = Depends(get_async_session)
):
    articles, total_items, total_pages = await ctrl.list_articles(db, page, per_page)
    items = [ArticleListItem.model_validate(a) for a in articles]
    meta = PaginationMeta(
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages
    )
    return PaginatedResponse(items=items, meta=meta)


# ------------------ GET ARTICLE BY SLUG ------------------
@router.get(
    "/{slug}",
    response_model=ArticleOut,
    summary="Получение статьи",
    description="Возвращает статью по уникальному slug."
)
async def get_article(
    slug: str,
    db: AsyncSession = Depends(get_async_session)
):
    article = await ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleOut.model_validate(article)


# ------------------ UPDATE ARTICLE ------------------
@router.put(
    "/{slug}",
    response_model=ArticleOut,
    summary="Обновление статьи",
    description="Обновляет статью, проверяя права текущего пользователя."
)
async def update_article(
    slug: str,
    data: ArticleUpdate,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id)
):
    article = await ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    check_author(article, user_id)  # Функция проверки автора должна быть определена

    updated = await ctrl.update_article(
        db,
        slug,
        user_id,
        title=data.title,
        description=data.description,
        body=data.body,
        tag_list=data.tagList
    )
    return ArticleOut.model_validate(updated)


# ------------------ DELETE ARTICLE ------------------
@router.delete(
    "/{slug}",
    response_model=dict,
    summary="Удаление статьи",
    description="Удаляет статью, если текущий пользователь является автором."
)
async def delete_article(
    slug: str,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id)
):
    article = await ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    check_author(article, user_id)
    await ctrl.delete_article(db, slug, user_id)
    return {"detail": "Article deleted successfully"}
