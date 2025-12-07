from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from src.models import Comment


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


async def get_comments_for_article(
    db: AsyncSession,
    article_id: int
):
    q = await db.execute(
        select(Comment).where(Comment.article_id == article_id)
    )
    return q.scalars().all()


async def get_comment_by_id(
    db: AsyncSession,
    comment_id: int
) -> Comment:
    q = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    comment = q.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment


async def delete_comment(
    db: AsyncSession,
    comment_id: int
):
    comment = await get_comment_by_id(db, comment_id)
    await db.delete(comment)
    await db.commit()
