from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.controllers import comment_controller, article_controller
from src.schemas.comment_schemas import CommentCreate, CommentOut
from src.utils.auth import get_current_user_id, check_author

router = APIRouter(
    prefix="/api/articles/{slug}/comments",
    tags=["Comments"]
)


# ------------------ CREATE COMMENT ------------------
@router.post("/", response_model=CommentOut, status_code=201)
async def create_comment(
    slug: str,
    data: CommentCreate,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id)
):
    # Получаем статью
    article = await article_controller.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Создаём комментарий
    comment = await comment_controller.create_comment(
        db=db,
        user_id=user_id,
        article_id=article.id,
        body=data.body
    )

    return CommentOut.model_validate(comment)


# ------------------ LIST COMMENTS ------------------
@router.get("/", response_model=List[CommentOut])
async def get_comments(
    slug: str,
    db: AsyncSession = Depends(get_async_session)
):
    article = await article_controller.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    comments = await comment_controller.get_comments_for_article(db, article.id)
    return [CommentOut.model_validate(c) for c in comments]


# ------------------ DELETE COMMENT ------------------
@router.delete("/{comment_id}", response_model=dict)
async def delete_comment(
    slug: str,
    comment_id: int,
    db: AsyncSession = Depends(get_async_session),
    user_id: int = Depends(get_current_user_id)
):
    # Проверяем, что статья существует
    article = await article_controller.get_article_by_slug(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Получаем комментарий
    comment = await comment_controller.get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Проверяем, что комментарий относится к статье
    if comment.article_id != article.id:
        raise HTTPException(
            status_code=400,
            detail="Комментарий не относится к этой статье"
        )

    # Проверяем права (автор)
    check_author(comment, user_id)

    await comment_controller.delete_comment(db, comment_id)
    return {"detail": "Комментарий удалён"}
