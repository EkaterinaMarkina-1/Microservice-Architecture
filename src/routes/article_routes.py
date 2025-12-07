from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.controllers import article_controller as ctrl
from src.schemas.article_schemas import (
    ArticleCreate,
    ArticleUpdate,
    ArticleOut,
    ArticleListItem
)
from src.utils.auth import get_current_user_id, check_author


router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.post("/", response_model=ArticleOut)
async def create_article(
    data: ArticleCreate,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id)
):
    article = await ctrl.create_article(
        db, user_id, data.title, data.description, data.body, data.tagList
    )
    return ArticleOut.model_validate(article)


@router.get("/", response_model=List[ArticleListItem])
async def list_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=50),
    db: AsyncSession = Depends(get_async_session)
):
    articles, _, _ = await ctrl.list_articles(db, page, per_page)
    return [ArticleListItem.model_validate(a) for a in articles]


@router.get("/{slug}", response_model=ArticleOut)
async def get_article(slug: str, db: AsyncSession = Depends(get_async_session)):
    article = await ctrl.get_article_by_slug(db, slug)
    return ArticleOut.model_validate(article)


@router.put("/{slug}", response_model=ArticleOut)
async def update_article(
    slug: str,
    data: ArticleUpdate,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id)
):
    article = await ctrl.get_article_by_slug(db, slug)
    check_author(article, user_id)

    updated = await ctrl.update_article(
        db,
        slug,
        user_id,
        data.title,
        data.description,
        data.body,
        data.tagList
    )
    return ArticleOut.model_validate(updated)


@router.delete("/{slug}", response_model=dict)
async def delete_article(
    slug: str,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id)
):
    article = await ctrl.get_article_by_slug(db, slug)
    check_author(article, user_id)

    await ctrl.delete_article(db, slug, user_id)
    return {"detail": "Статья удалена"}
