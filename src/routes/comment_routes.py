from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.controllers import comment_controller as comments_ctrl
from src.controllers import article_controller as articles_ctrl
from src.utils.auth import get_current_user_id, check_author

router = APIRouter(prefix="/api/articles/{slug}/comments", tags=["comments"])

@router.post("/", response_model=dict)
async def create_comment(
    slug: str,
    body: str,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    comment = await comments_ctrl.create_comment(db, user_id, article.id, body)
    return {"id": comment.id, "body": comment.body, "author_id": user_id}

@router.get("/", response_model=List[dict])
async def get_comments(slug: str, db: AsyncSession = Depends(get_db)):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    comments = await comments_ctrl.get_comments_for_article(db, article.id)
    return [{"id": c.id, "body": c.body, "author_id": c.author_id} for c in comments]

@router.delete("/{comment_id}", response_model=dict)
async def delete_comment(
    slug: str,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    article = await articles_ctrl.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    comment = await comments_ctrl.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    if comment.article_id != article.id:
        raise HTTPException(status_code=400, detail="Комментарий не относится к этой статье")

    check_author(comment, user_id)
    await comments_ctrl.delete_comment(db, comment_id)
    return {"detail": "Комментарий удалён"}
