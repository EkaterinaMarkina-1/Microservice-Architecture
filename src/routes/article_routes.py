from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.controllers import article_controller as articles_ctrl
from src.utils.auth import get_current_user_id, check_author

router = APIRouter(prefix="/api/articles", tags=["articles"])

@router.post("/", response_model=dict)
async def create_article(
    title: str,
    description: str,
    body: str,
    tagList: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    article = await articles_ctrl.create_article(db, user_id, title, description, body, tagList)
    return {"slug": article.slug, "title": article.title, "description": article.description}

@router.get("/", response_model=List[dict])
async def list_articles(
    page: int = Query(1, ge=1),
    per_page: int = Query(15, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    try:
        articles, _, _ = await articles_ctrl.list_articles(db, page, per_page)
        return [{"slug": a.slug, "title": a.title, "author_id": a.author_id} for a in articles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статей: {str(e)}")

@router.get("/{slug}", response_model=dict)
async def get_article(slug: str, db: AsyncSession = Depends(get_db)):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return {
        "slug": article.slug,
        "title": article.title,
        "description": article.description,
        "body": article.body,
        "author_id": article.author_id
    }

@router.put("/{slug}", response_model=dict)
async def update_article(
    slug: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    body: Optional[str] = None,
    tagList: Optional[List[str]] = None,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    check_author(article, user_id)
    article = await articles_ctrl.update_article(db, slug, user_id, title, description, body, tagList)
    return {"slug": article.slug, "title": article.title, "description": article.description}

@router.delete("/{slug}", response_model=dict)
async def delete_article(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    check_author(article, user_id)
    await articles_ctrl.delete_article(db, slug, user_id)
    return {"detail": "Статья удалена"}
