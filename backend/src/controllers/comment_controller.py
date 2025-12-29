from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Comment


# ------------------ CREATE COMMENT ------------------
async def create_comment(
    db: AsyncSession,
    user_id: int,
    article_id: int,
    body: str
) -> Comment:
    comment = Comment(
        author_id=user_id,
        article_id=article_id,
        body=body
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


# ------------------ GET COMMENTS FOR ARTICLE ------------------
async def get_comments_for_article(
    db: AsyncSession,
    article_id: int
) -> List[Comment]:
    q = await db.execute(
        select(Comment)
        .where(Comment.article_id == article_id))
    return q.scalars().all()


# ------------------ GET COMMENT BY ID ------------------
async def get_comment_by_id(
    db: AsyncSession,
    comment_id: int,
    raise_if_missing: bool = True
) -> Optional[Comment]:
    q = await db.execute(
        select(Comment)
        .where(Comment.id == comment_id)
        .options(selectinload(Comment.author))
    )
    comment = q.scalar_one_or_none()
    if raise_if_missing and not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment


# ------------------ UPDATE COMMENT ------------------
async def update_comment(
    db: AsyncSession,
    comment_id: int,
    user_id: int,
    body: Optional[str] = None
) -> Comment:
    comment = await get_comment_by_id(db, comment_id)
    if comment.author_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    if body is not None:
        comment.body = body

    await db.commit()
    await db.refresh(comment)
    return comment


# ------------------ DELETE COMMENT ------------------
async def delete_comment(
    db: AsyncSession,
    comment_id: int,
    user_id: Optional[int] = None
):
    comment = await get_comment_by_id(db, comment_id)

    if user_id is not None and comment.author_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    await db.delete(comment)
    await db.commit()
